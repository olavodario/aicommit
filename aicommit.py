import sys
import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv #Opcional, para carregar a .env

#Carrega variáveis de ambiente de um arquivo .env (Opcional)
#Útil para desenvolvimento local se não quiser setar a variável globalmente

load_dotenv ()

# --- Configuração ---
#Pega a API Key da variável de ambiente (Gemini)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    print("Configure-a com sua API Key do Google AI Studio.")
    sys.exit(1)#Sai do script com código de erro

genai.configure(api_key=API_KEY)
# Modelo a ser usado (pode precisar ajustar conforme disponibilidade/preferência)
model = genai.GenerativeModel ('gemini-1.5-flash-latest')
#-------------------------

def get_staged_diff ():
    """Executa 'git diff --staged' e retorna a saída ou None se ouver erro."""
    try:
        # '--diff-algorithm=minimal' pode ajudar a gerar diffs mais concisos 
        result = subprocess.run(
            ['git', 'diff', '--staged', '--diff-algorithm=minimal'],
            capture_output=True,
            text=True,
            check=True, # Levanta execução se o commando git falhar
            encoding='utf-8' #Garante decodificação correta do texto
        )
        return result.stdout
    except FileNotFoundError:
        print("Erro: Comando 'git' não encontrado. O Git está instalado e no PATH?")
        return None
    except subprocess.CalledProcessError as e:
        #Erros comuns: não é um repositório git, etc.
        print(f"Erro ao executar git diff: {e.stderr}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao obter diff: {e}")
        return None
    
def generate_commit_message(diff):
    """Usa a IA para gerar uma mensagem de commit baseada no diff."""
    if not diff:
        print("Nenhuma mudança detectada no stage (git diff --staged está vazio).")
        return None
    
    # Prompt para a IA
    # Ajuste o prompt para obter melhores resultados
    # Pedir formato Conventional Commits é uma boa prática
    prompt = f"""
    Analise o seguinte diff de mudanças que foram adicionadas ao stage do Git (`git diff --staged`).
    Gere uma mensagem de commit concisa e informativa em português(br), seguindo o padrão Conventional Commits (ex: feat:, fix:, chore:, docs:, style:, refactor:, test:).
    A mensagem deve ter um título curto (máximo 50 caracteres) e, opcionalmente, um corpo explicando melhor (separado por linha em branco).

    Diff:
    '''diff
    {diff}
    '''

    Mensagem de commit gerada:
    """
    #Fim do prompt

    print("🤖 Gerando mensagem de commit com IA...")
    try:
        response = model.generate_content(prompt)
        # Tratamento básico para extrair o texto limpo
        commit_message = response.text.strip()
        # Remove ``` que a IA pode adicionar ao redor da mensagem
        if commit_message.startswith("```") and commit_message.endswith("```"):
            commit_message = commit_message[3:-3].strip()
        # Remove possíveis prefixos indesejados que a IA pode adicionar
        if commit_message.lower().startswith("mensagem de commit gerada:"):
            commit_message = commit_message[len("mensagem de commit gerada:"):].strip()

        return commit_message
    except Exception as e:
        print(f"Erro ao chamar a API da IA: {e}")
        # Tenta mostrar detalhes do erro da resposta, se disponíveis
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Detalhes da API: {e.response.text}")
            return None
    
def run_git_commit(message):
        
        """Executa 'git commit -m {message}'."""
        if not message: 
            print("Não foi possível gerar a mensagem de commit. Abortando missão...")
            return False
        
        print(f"\n📝 Mensagem gerada:\n---\n{message}\n---\n")

        #Adicionar confirmação
        confirm = input("Prosseguir com o commit? (s/N): ").lower().strip()
        if confirm != 's':
            print("Commit cancelado pelo usuário.")
            return False
        
        print("🚀 Executando o commit...")
        try:
            #Usa splitlines para passar a mensagem corretamente, especialmente se tiver múltiplas linhas
            lines = message.splitlines()
            cmd = ['git', 'commit']
            for line in lines:
                cmd.extend(['-m', line]) # Adiciona cada linha como como um -m separado

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True, # Levanta execução se o commando git falhar
                encoding='utf-8' #Garante decodificação correta do texto
            )
            print("\n✅ Commit realizado com sucesso!")
            print(result.stdout) # Mostra a saída do commit
            return True
        except subprocess.CalledProvessError as e:
            print("\n❌ Erro ao executar git commit:")
            print(e.stderr)
            print(e.stdout)
            return False
        except Exception as e:
            print(f"Erro inesperado ao commitar: {e}")
            return False
        
# --- Fluxo Principal ---
if __name__ == "__main__":
    diff_output = get_staged_diff()

    if diff_output is None:
        #Mensagem de erro já foi impressa nas funções!
        sys.exit(1) # Sai se não conseguiu obter o diff

    if not diff_output.strip():
        print("Nada para commitar (git diff --staged está vazio).")
        sys.exit(0) # Sai normalmente se não há nada a commitar

    commit_msg = generate_commit_message(diff_output)

    if commit_msg:
        success = run_git_commit(commit_msg)

        if not success:
            sys.exit(1) # Sai com erro se o commit falhou 
    
    else: 
        print("Não foi possível gerar ou confirmar a mensagem. Commit não realizado.")
        sys.exit(1) # Sai com erro se a mensagem não foi gerada/confirmada

