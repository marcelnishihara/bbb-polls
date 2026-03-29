# BBB Polls

Este repositório contém o código-fonte de uma Cloud Function desenvolvida para o reality show Big Brother Brasil (BBB). A Cloud Function é projetada para extrair dados parciais de enquetes promovidas pela [Splash](https://www.uol.com.br/splash/), portal de entretenimento da [UOL](https://www.uol.com.br/), e publicá-los na conta [@bbb_polls no X (Twitter)](https://twitter.com/bbb_polls/).

## Sobre o Big Brother Brasil

O BBB é um dos reality shows mais populares do Brasil, e as enquetes relacionadas ao programa geram grande interesse e engajamento nas redes sociais. Esta Cloud Function foi desenvolvida para automatizar a coleta de dados das enquetes, tornando mais fácil acompanhar a evolução das preferências do público ao longo do programa.

## Funcionalidades Principais

- **Extração de Dados de Enquetes:** A Cloud Function faz uma requisição à página da enquete vigente na semana da [Splash (Uol)](https://www.uol.com.br/splash/) para obter seus dados parciais.
- **Publicação de Tweets:** Além de armazenar os dados, a função também publica tweets na conta [@bbb_polls no X (Twitter)](https://twitter.com/bbb_polls/), compartilhando informações atualizadas sobre as enquetes.

## Informação Relevante Sobre o Projeto

- Desde a segunda semana de março de 2026, conforme relatado na [_Issue_ #22](https://github.com/marcelnishihara/bbb-polls/issues/22), toda tentativa de postar um tuíte via API retornava um _status code_ `503` com a mensagem `Service Unavailable`.
- Após ler [relatos de pessoas encontrando o mesmo erro desde o mês anterior](https://devcommunity.x.com/t/503-errors-since-2-28/258704), optei pela exclusão do _app_ (vinculado ao plano gratuito) na página do [Developer Console](https://console.x.com/) e aprofundar a investigação sobre o que possa gerar esse erro sem sentido em um primeiro momento.
- A resposta para isso está no [anúncio publicado pela funcionária do X, @taycaldwell](https://devcommunity.x.com/t/announcing-the-launch-of-x-api-pay-per-use-pricing/256476), onde, em resumo, o X descontinuou o plano gratuito e optou por uma solução `Pay-Per-Use`.
- Dessa forma, continuarei rodando essa aplicação durante essa edição do Big Brother Brasil sem uma solução automática de postagem dos resultados no X. Ao final da temporada, encerrarei esse projeto até segundo momento.
