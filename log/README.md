# Diretório de Logs (`log/`)

Este diretório é destinado ao armazenamento persistente de arquivos de log gerados durante a execução da Cloud Function e dos scripts de teste automatizados. Os registros são salvos individualmente em formato JSON estruturado por meio do método estático `Helpers.log()`.

## Padrão de Nomenclatura dos Arquivos

Os arquivos gravados neste diretório seguem a convenção estrita de nomenclatura baseada no prefixo de evento e no timestamp formatado no fuso horário `America/Sao_Paulo`:

```
<prefixo>_<AAAA_MM_DD_HH_MM_SS_ffffff>.<extensao>
```

Exemplo:
`log_poll_2026_01_15_22_30_05_123456.json`

## Tipos de Logs Gerados

A aplicação gera diferentes categorias de logs identificadas pelos seus respectivos prefixos:

### 1. `log_poll_*.json`
Gerado durante a execução padrão da função (`main.py` -> `process()`). Contém o snapshot completo dos dados extraídos da enquete no portal Splash/UOL.

**Estrutura típica:**
```json
{
    "todayIs": "2026_01_15_22_30_05_123456",
    "url": "https://www.uol.com.br/splash/bbb/enquetes/...",
    "title": "Quem você quer eliminar no paredão?",
    "totalOfVotes": 1250000,
    "players": [
        {
            "position": 1,
            "id": 101,
            "name": "Participante A",
            "percentage": 52.34
        },
        {
            "position": 2,
            "id": 102,
            "name": "Participante B",
            "percentage": 47.66
        }
    ]
}
```

### 2. `log_bad_request_*.json`
Gerado quando uma requisição falha na validação de segurança ou integridade dos cabeçalhos HTTP (`RequestAnalysis.is_valid_request()`).

**Estrutura típica:**
```json
{
    "badRequest": true,
    "todayIs": "2026_01_15_22_30_05_123456",
    "explanation": [
        {
            "isValidUUID": false,
            "error": "If \"isValidUUID\" is False, the UUID is incorrect"
        }
    ]
}
```

### 3. `log_tweet_data_*.json`
Gerado quando a postagem automática na API do X é executada com sucesso ou erro, registrando o retorno completo da biblioteca Tweepy e os metadados do tweet.

### 4. `log_tests_error_*.json`
Gerado pelo script de testes contínuos (`tests/tests.py`) em caso de exceções não tratadas durante o ciclo de requisições periódicas.

## Consumo e Processamento dos Logs

Os arquivos JSON presentes neste diretório são utilizados como fonte de dados para rotinas de consolidação e análise temporal:

- **`tests/create_logs_database.py`:** Faz a leitura de todos os arquivos com prefixo `log_poll_`, extrai o histórico de votação e consolida os dados em uma base única (`database/bbb_2024_log_database.json`).
- **`tests/log_join.py`:** Filtra os logs por um endpoint específico de enquete, ordena cronologicamente os parciais e gera o arquivo `flourish_bar_chart_race.csv` para criação de animações visuais de evolução dos votos.

## Manutenção

Os arquivos deste diretório funcionam como logs brutos de auditoria e telemetria local. Para novos ambientes, recomenda-se manter o diretório criado no controle de versão (via este `README.md`) e ignorar os arquivos de log individuais caso deseje evitar acúmulo de artefatos temporários no repositório.