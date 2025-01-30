# BBB Polls

Este repositório contém o código-fonte de uma Cloud Function desenvolvida para o reality show Big Brother Brasil (BBB). A Cloud Function é projetada para extrair dados parciais de enquetes promovidas pela [Splash](https://www.uol.com.br/splash/), portal de entretenimento da [UOL](https://www.uol.com.br/), e publicá-los na conta [@bbb_polls no X (Twitter)](https://twitter.com/bbb_polls/).

## Sobre o Big Brother Brasil

O BBB é um dos reality shows mais populares do Brasil, e as enquetes relacionadas ao programa geram grande interesse e engajamento nas redes sociais. Esta Cloud Function foi desenvolvida para automatizar a coleta de dados das enquetes, tornando mais fácil acompanhar a evolução das preferências do público ao longo do programa.

## Funcionalidades Principais

- **Extração de Dados de Enquetes:** A Cloud Function faz uma requisição à página da enquete vigente na semana da [Splash (Uol)](https://www.uol.com.br/splash/) para obter seus dados parciais.
- **Publicação de Tweets:** Além de armazenar os dados, a função também publica tweets na conta [@bbb_polls no X (Twitter)](https://twitter.com/bbb_polls/), compartilhando informações atualizadas sobre as enquetes.
