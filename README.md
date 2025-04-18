# AICommit: Gerador Inteligente de Mensagens de Commit

**AICommit** é uma ferramenta de linha de comando (CLI) que utiliza inteligência artificial (Google Gemini) para gerar automaticamente mensagens de commit Git com base nas suas alterações em stage (`git diff --staged`). Ele visa agilizar o processo de commit, sugerindo mensagens informativas e padronizadas(você pode utilizar outras IA's tbm, basta apenas mudar a biblioteca do google gemini pela a da IA escolhida, e configurar seu token).

**Última atualização:** 12 de abril de 2025

---

##Funcionalidades

*Gera mensagens de commit automaticamente usando a API do Google Gemini. 
*Analisa as alterações preparadas para commit (staged changes). 
*Formata as mensagens de commit (tentando seguir o padrão [Conventional Commits](https://www.conventionalcommits.org/)).
*Exibe a mensagem derada e **pede confirmação** antes de realizar o commit. 
*Integra-se facilmente ao seu fluxo de trabalho Git existente.
*Ativavel atravel do comando 'aicommit' via linha de comando.

##Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Python 3:** Versão 3.7 ou superior. [Dowload Python](https://www.python.org/downloads/).
2. **Git:** O sistema de controle de versão. [Dowload Git](https://git-scm.com/downloads).
    **Importante:** Certifique-se que o Git esteja acessível através do PATH do seu sistema.
3. **pip:** O gerenciador de pacotes do Python (geralmente vem com o Python).
4. **Conta Google e API Key para usar o modelo Gemini. Obtenha gratuitamente em [Google AI Studio](https://aistudio.google.com/app/apikey).

## Instalação

1. **Clone ou baixe o Script:**
    *Salve o código Python fornecido anteriormente em um arquivo chamado 'aicommit.py' em ul local permanente no seu computador (ex:'~/scripts/' no Linux/macOS ou 'C:\Users\SeuUsuario\Scripts\' no Windows).

2. **Instale as Dependências Python:**
    Abra seu terminal ou prompt de comando (CMD) e execute:
    ```bash
    pip install google-generativeai python-dotenv
    ```
    *(A dependência `python-dotenv` é usada opcionalmente no script para carregar variáveis de um arquivo `.env`, mas o método principal é via variável de ambiente do sistema).*

3.  **Configure a API Key:**
    * **NUNCA** coloque sua API Key diretamente no código! Configure-a como uma variável de ambiente chamada `GOOGLE_API_KEY`.
    * **Linux/macOS:** Adicione `export GOOGLE_API_KEY='SUA_API_KEY_AQUI'` ao seu `~/.bashrc`, `~/.zshrc` ou arquivo de perfil equivalente e recarregue o shell (`source ~/.bashrc`).
    * **Windows:** Use as configurações de "Variáveis de Ambiente" do sistema para criar uma nova variável de usuário chamada `GOOGLE_API_KEY` com sua chave como valor, ou use os comandos `setx GOOGLE_API_KEY "SUA_API_KEY_AQUI"` (CMD) ou `[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'SUA_API_KEY_AQUI', [System.EnvironmentVariableTarget]::User)` (PowerShell). **Lembre-se de reiniciar o terminal após definir a variável.**

4.  **Torne o Script Executável e Acessível:**
    O objetivo é poder chamar `aicommit` de qualquer diretório no terminal.

    * **Linux/macOS:**
        1.  Dê permissão de execução: `chmod +x /caminho/para/aicommit.py`
        2.  Mova ou crie um link simbólico para um diretório no seu PATH:
            * Ex (mover): `mv /caminho/para/aicommit.py ~/.local/bin/aicommit` (certifique-se que `~/.local/bin` está no PATH)
            * Ex (link): `sudo ln -s /caminho/completo/para/aicommit.py /usr/local/bin/aicommit`

    * **Windows:**
        1.  **Opção A (Recomendado):** Adicione o diretório onde você salvou `aicommit.py` (ex: `C:\Users\SeuUsuario\Scripts`) à sua variável de ambiente `Path`. Depois, crie um arquivo `aicommit.bat` na mesma pasta com o conteúdo `@python "%~dp0aicommit.py" %*`.
        2.  **Opção B:** Adicione o diretório à variável `Path` e certifique-se de que os arquivos `.py` estão associados ao interpretador Python. Você pode precisar chamar `aicommit.py`. A opção com `.bat` garante que você possa chamar apenas `aicommit`.

## Configuração Adicional

* **Prompt da IA:** Você pode personalizar o prompt enviado à IA editando a variável `prompt` dentro do script `aicommit.py` para ajustar o estilo ou o formato das mensagens geradas.
* **Modelo Gemini:** O script usa `gemini-1.5-flash-latest` por padrão. Você pode alterar para outro modelo disponível na API do Google AI mudando a linha `model = genai.GenerativeModel('gemini-1.5-flash-latest')`.

## Como Usar

1.  Navegue até o diretório do seu repositório Git usando o terminal.
2.  Faça as alterações desejadas nos seus arquivos.
3.  Adicione as alterações ao stage do Git:
    ```bash
    git add .
    # ou git add <arquivo_especifico>
    ```
4.  Execute o AICommit:
    ```bash
    aicommit
    ```
5.  O script buscará as alterações, enviará para a IA e exibirá a mensagem de commit sugerida.
6.  Revise a mensagem cuidadosamente.
7.  Se estiver satisfeito, digite `s` e pressione Enter para confirmar e realizar o commit.
8.  Se quiser cancelar, digite `n` ou apenas pressione Enter.
9.  **Importante:** O `aicommit` **NÃO** faz `git push`. Você precisará fazer isso manualmente depois, se desejar enviar seus commits para o repositório remoto:
    ```bash
    git push
    ```

## Como Funciona (Resumo Técnico)

1.  O script executa `git diff --staged` para capturar as mudanças preparadas.
2.  Envia esse `diff` como parte de um prompt para a API do Google Gemini.
3.  Recebe a sugestão de mensagem de commit gerada pela IA.
4.  Exibe a mensagem e aguarda a confirmação do usuário (`s/N`).
5.  Se confirmado ('s'), executa `git commit -m "Mensagem Gerada"` (usando múltiplos `-m` para mensagens com várias linhas).

## Considerações Importantes

* **Qualidade da IA:** A mensagem gerada é uma sugestão. A qualidade pode variar dependendo da complexidade das alterações e do modelo de IA. **Sempre revise a mensagem antes de confirmar.**
* **Segurança da API Key:** Proteja sua `GOOGLE_API_KEY`. Não a compartilhe e não a coloque diretamente no código.
* **Custos da API:** Esteja ciente dos limites de uso gratuito e dos possíveis custos associados ao uso da API do Google Gemini.
* **Não Faz Push:** Lembre-se que `git push` é uma etapa manual separada.
* **Sem Garantias:** Esta é uma ferramenta auxiliar. Use por sua conta e risco. Faça backup do seu trabalho.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

Copyright (c) 2025 Olavo Ribeiro Gomes Dario.
