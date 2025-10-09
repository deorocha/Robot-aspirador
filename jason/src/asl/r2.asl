// Crenças iniciais
pos(3,3).

// Comportamento do incinerador
+!manter_posicao.

+lixo_para_incinerar : true <- 
    .print("Incinerando lixo...");
    incinerate;
    .print("Lixo incinerado com sucesso!").