# BBB Polls

Este repositório contém o código-fonte de uma Cloud Function desenvolvida para o reality show Big Brother Brasil (BBB). A Cloud Function é projetada para extrair dados parciais de enquetes promovidas pela [Splash](https://www.uol.com.br/splash/), portal de entretenimento da [UOL](https://www.uol.com.br/), e publicá-los tweets na conta [@bbb_polls no X (Twitter)](https://twitter.com/bbb_polls/).

## Sobre o Big Brother Brasil

O BBB é um dos reality shows mais populares do Brasil, e as enquetes relacionadas ao programa geram grande interesse e engajamento nas redes sociais. Esta Cloud Function foi desenvolvida para automatizar a coleta de dados das enquetes, tornando mais fácil acompanhar a evolução das preferências do público ao longo do programa.

## Funcionalidades Principais

- **Extração de Dados de Enquetes:** A Cloud Function faz uma requisição à página da enquete vigente na semana da [Splash (Uol)](https://www.uol.com.br/splash/) para obter seus dados parciais.

- **Publicação de Tweets:** Além de armazenar os dados, a função também publica tweets na conta [@bbb_polls no X (Twitter)](https://twitter.com/bbb_polls/), compartilhando informações atualizadas sobre as enquetes.

## Rodando o bbb-polls Localmente

### Preparando o Ambiente

  - #### Criando um Twitter Bot

    - Siga a [documentação oficial](https://developer.twitter.com/en/docs/tutorials/how-to-create-a-twitter-bot-with-twitter-api-v2) do X (Twitter) para criar um bot utilizando a v2 do Twitter API.
    - Naturalmente esse passo é obrigatório se seu objetivo é criar tweets com base nas informações coletadas.

  - #### PowerShell (Microsoft Windows)

    - `PS > py -m venv env`
    - `PS > .\env\Script\activate`
    - `(env) PS > py -m pip install --upgrade pip` (Optional)
    - `(env) PS > py -m pip install -r  requirements.txt`

  - #### Credenciais

    - Registre os valores para cada uma as variáveis de ambiente registradas no arquivo `./credentials/creds.ps1`;
    - Crie as variáveis dentro do ambiente virtual do projeto, criado no primeiro subtópico da seção `PowerShell (Microsft Windows)`.
    - Para saber qual valor definir para a chave `PROJECT_UUID`, vide o tópico `Fazendo uma Requisição para o functions-framework`, 
    - Considere `https://storage.cloud.google.com/bbb-polls` como valor para a variável de ambiente `SOURCES_JSON_FILE_URL_BASE`.

  - #### Utilizando o `functions-framework`

    - Como se trata de uma Cloud Function, executar este projeto localmente demanda um framework específico que foi projetado pelo próprio time do Google Cloud Platform (GCP);
    - Assim, siga a [documentação oficial do `functions-framework`](https://github.com/GoogleCloudPlatform/functions-framework-python) para realizar sua instalação e aprender como executá-lo adequadamente.


### Fazendo uma Requisição para o `functions-framework`

  -  Utilize o código do módulo `./tests/tests.py` para realizar sua requisição. Substitua o valor da variável `URL` de `''` para o endereço de seu `localhost` e preencha os valores das chaves do objeto utilizado como o cabeçalho (_header_) da requisição e seus valores são todos do tipo `string`.
  - O objeto utilizado como _header_ da requisião contém as seguintes chaves obrigatórias:
    - `projectUUID`: Trata-se do mesmo valor que você registrou para a variável de ambiente `PROJECT_UUID`. O objetivo dela é apenas criar uma pequena camada de segurança para evitar acionamentos indesejados da Cloud Function. Recomenda-se o uso de um [UUID](https://pt.wikipedia.org/wiki/Identificador_%C3%BAnico_universal);
    - `tweet`: Trata-se de uma chave que espera receber a string `'1'` caso você deseja criar um tweet com o resultado da enquete ou `'0'` caso você queira fazer apenas o processo de extração dos dados ou se você não possui um [Twitter Bot](https://developer.twitter.com/en/docs/tutorials/how-to-create-a-twitter-bot-with-twitter-api-v2);
    - `pollIndex`: É o número do paredão que você deseja consultar. Exemplo: caso queira extrair os dados do 3º paredão da edição, para definir a `string` `'3'` como valor para esta chave;
    - `housematesNumber`: Número de pessoas envolvidas na votação;
    - `counterLimit`: Número de pessoas que deverão ser listadas no tweets. Algumas enquetes envolvem muitos participante, o que inviabiliza a criação do tweet por conta do [limite de 280 caracteres](https://developer.twitter.com/en/docs/counting-characters). Caso o valor da `string` seja `'0'`, isso indicará que o tweet a ser criado deverá considerar o número de participantes envolvidos na enquete, ou seja, o valor para `housematesNumber`;
    - `sourceWebPage`: Você deve especificar a origem dos dados a serem extraídos. Como este código conseguiu de maneira sistêmica a extração da enquetes da [Splash (Uol)](https://www.uol.com.br/splash/), o único valor aceito, infelizmente, é a `string` `'splash'`;
    - `sourcesJsonFile`: É o caminho (_path_) do endereço do arquivo `JSON` onde estão listadas todas as URLs das enquestes da [Splash (Uol)](https://www.uol.com.br/splash/). Um exemplo de valor para essa string é `sources/2023_04_24a.json`, pois se trata do arquivo `JSON` que lista todas as enquetes produzidas para a temporada 23 do BBB, ocorrida entre 16 de janeiro e 25 de abril de 2023:
      - A base da URL do aquivo `JSON` é o valor definido para a variável de ambiente `SOURCES_JSON_FILE_URL_BASE`.
