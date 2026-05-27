# Upload do simulado para Google Docs via OAuth

Este guia usa o script local:

```bash
scripts/upload_to_google_drive.py
```

Ele faz upload de um arquivo `.docx` para o Google Drive e, por padrão, converte o arquivo para um documento nativo do Google Docs.

## 1. Criar projeto no Google Cloud

1. Acesse: <https://console.cloud.google.com/>
2. Crie um novo projeto ou selecione um projeto existente.
3. Guarde o nome do projeto apenas para referência.

## 2. Ativar a API do Google Drive

1. No Google Cloud Console, vá em **APIs & Services**.
2. Clique em **Enable APIs and services**.
3. Procure por **Google Drive API**.
4. Clique em **Enable**.

## 3. Configurar tela de consentimento OAuth

1. Vá em **APIs & Services → OAuth consent screen**.
2. Escolha **External** se for conta Google pessoal.
3. Preencha o mínimo obrigatório:
   - App name
   - User support email
   - Developer contact information
4. Em **Test users**, adicione o e-mail Google que fará o upload.
5. Salve.

Observação: enquanto o app estiver em modo de teste, apenas usuários adicionados em **Test users** poderão autorizar.

## 4. Criar credenciais OAuth

1. Vá em **APIs & Services → Credentials**.
2. Clique em **Create Credentials → OAuth client ID**.
3. Em **Application type**, selecione **Desktop app**.
4. Dê um nome, por exemplo: `Mirror Local Drive Upload`.
5. Clique em **Create**.
6. Baixe o arquivo JSON das credenciais.
7. Salve o arquivo como:

```text
docs/provas/ciencias/p1/google-oauth-credentials.json
```

> Não commite esse arquivo. Ele contém credenciais do seu app OAuth.

## 5. Rodar o script local

Do diretório raiz do projeto, execute:

```bash
uv run scripts/upload_to_google_drive.py \
  docs/provas/ciencias/p1/simulado-p2-ciencias-01.docx \
  --credentials docs/provas/ciencias/p1/google-oauth-credentials.json \
  --token docs/provas/ciencias/p1/.google-drive-token.json \
  --name "Simulado P2 Ciências 01"
```

Na primeira execução:

1. O navegador será aberto.
2. Faça login na sua conta Google.
3. Autorize o acesso solicitado.
4. O script fará upload do `.docx` e converterá para Google Docs.
5. O terminal mostrará o link do documento.

## 6. Enviar para uma pasta específica do Drive

Se quiser criar o documento dentro de uma pasta específica, copie o ID da pasta no Google Drive e use `--folder-id`:

```bash
uv run scripts/upload_to_google_drive.py \
  docs/provas/ciencias/p1/simulado-p2-ciencias-01.docx \
  --credentials docs/provas/ciencias/p1/google-oauth-credentials.json \
  --token docs/provas/ciencias/p1/.google-drive-token.json \
  --name "Simulado P2 Ciências 01" \
  --folder-id "ID_DA_PASTA"
```

## 7. Upload sem converter para Google Docs

Se quiser subir apenas como arquivo Word `.docx`, use:

```bash
uv run scripts/upload_to_google_drive.py \
  docs/provas/ciencias/p1/simulado-p2-ciencias-01.docx \
  --credentials docs/provas/ciencias/p1/google-oauth-credentials.json \
  --token docs/provas/ciencias/p1/.google-drive-token.json \
  --name "Simulado P2 Ciências 01" \
  --no-convert
```

## Segurança

- Não informe usuário e senha do Google em nenhum script.
- Use OAuth.
- Não commite arquivos como:
  - `google-oauth-credentials.json`
  - `.google-drive-token.json`
- O escopo usado pelo script é `drive.file`, que permite criar e gerenciar arquivos criados pelo próprio app, sem liberar acesso amplo a todo o Drive.
