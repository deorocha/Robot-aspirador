# Sistema de Robô Incinerador

## Descrição
Sistema multiagente com Jason para limpeza de ambiente usando dois robôs:
- R1: Robô coletor que busca lixos e os leva ao incinerador
- R2: Robô incinerador que destrói os lixos

## Especificações
- Grid: 7x7 células
- Posição inicial R1: (0,0)
- Posição R2: (3,3) - fixa
- Lixos: (1,2), (3,5), (4,4), (6,6)
- Moeda: (4,5)

## Como Executar
1. Certifique-se de ter Jason instalado
2. Execute: `jason incinerator_robot.mas2j`

## Comportamento dos Agentes

### R1 (Coletor)
1. Inicia em (0,0)
2. Procura sistematicamente por lixos
3. Coleta lixo quando encontrado
4. Leva lixo ao R2 em (3,3)
5. Repete até não haver mais lixos
6. Busca e coleta moeda em (4,5)

### R2 (Incinerador)
1. Permanece em (3,3)
2. Incinera lixos quando depositados