# tweets/

Este diretório armazena os **registros históricos das mensagens** geradas pela Cloud Function para publicação no X (Twitter).

## Estrutura dos Arquivos

Cada arquivo é criado pela função [`Helpers.log()`](../classes/helpers.py) sempre que uma requisição é recebida com o cabeçalho `Tweet: true`. O nome segue o padrão:

```
log_tweet_msg_AAAA_MM_DD_HH_MM_SS_ffffff.txt
```

| Segmento | Descrição |
| :--- | :--- |
| `log_tweet_msg` | Prefixo fixo que identifica o tipo de registro |
| `AAAA_MM_DD` | Data da coleta no fuso horário `America/Sao_Paulo` |
| `HH_MM_SS_ffffff` | Hora, minuto, segundo e microssegundo da coleta |

## Conteúdo de Cada Arquivo

O texto gravado corresponde ao conteúdo completo que seria publicado como tweet — composto pelo método [`Twitter.compose_msg()`](../classes/twitter.py) — e inclui:

- Título da enquete ativa com menção a `@Splash_UOL` e hashtags `#BBB26` e `#RedeBBB`
- Ranking dos participantes mais votados (até o limite definido pelo cabeçalho `Limit`)
- Percentual residual agregado dos demais participantes
- Total de votos computados no momento da coleta
- Timestamp da extração no formato `DD/MM/AAAA às HH:MM:SS`

### Exemplo de Conteúdo

```
Parcial da enquete @Splash_UOL #BBB26: "Quem você quer eliminar?" #RedeBBB

1º Participante A: 52,30%
2º Participante B: 30,10%
3º Participante C: 12,45%

Os demais somam 5,15%
Total de Votos: 1.234.567
🕒 15/01/2026 às 14:35:00
```

## Observação

> [!NOTE]
> A partir de março de 2026, a publicação efetiva via API do X foi pausada em decorrência da descontinuação do plano gratuito (ver [_Issue_ #22](https://github.com/marcelnishihara/bbb-polls/issues/22)). Os arquivos neste diretório registram as mensagens que *seriam* postadas, servindo como telemetria local das execuções da Cloud Function.