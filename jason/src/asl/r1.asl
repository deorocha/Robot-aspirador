// Crenças iniciais
pos(0,0).           // Posição inicial do R1
r2_pos(3,3).        // Posição do incinerador (R2)
moeda_pos(4,5).     // Posição da moeda

// Metas iniciais
!iniciar_limpeza.

// Plano principal
+!iniciar_limpeza <- 
    .print("Iniciando limpeza do ambiente");
    !procurar_lixo.

// Procura por lixos
+!procurar_lixo <- 
    .print("Procurando por lixos...");
    ?lixo_na_posicao;
    .print("Lixo encontrado! Coletando...");
    pick_lixo;
    .print("Lixo coletado. Levando para incinerador...");
    !levar_ao_incinerador.
    
+!procurar_lixo <- 
    .print("Nenhum lixo nesta posição. Continuando busca...");
    !explorar;
    !procurar_lixo.

// Leva lixo ao incinerador
+!levar_ao_incinerador <- 
    ?r2_pos(X,Y);
    ?pos(AtualX, AtualY);
    (AtualX != X | AtualY != Y);
    !navegar_para(X,Y);
    !levar_ao_incinerador.
    
+!levar_ao_incinerador <- 
    ?no_incinerador;
    .print("Chegou ao incinerador. Depositando lixo...");
    drop_lixo;
    .print("Lixo depositado. Esperando incineração...");
    +lixo_depositado;
    !verificar_lixos_restantes.

// Navegação para coordenadas específicas
+!navegar_para(DestX, DestY) : pos(AtualX, AtualY) & AtualX < DestX <- 
    move(down);
    ?pos(AtualX, AtualY).
    
+!navegar_para(DestX, DestY) : pos(AtualX, AtualY) & AtualX > DestX <- 
    move(up);
    ?pos(AtualX, AtualY).
    
+!navegar_para(DestX, DestY) : pos(AtualX, AtualY) & AtualY < DestY <- 
    move(right);
    ?pos(AtualX, AtualY).
    
+!navegar_para(DestX, DestY) : pos(AtualX, AtualY) & AtualY > DestY <- 
    move(left);
    ?pos(AtualX, AtualY).

// Exploração do grid
+!explorar : pos(X,Y) & X < 6 & not lixo_na_posicao <- 
    move(down).
    
+!explorar : pos(X,Y) & X == 6 & Y < 6 & not lixo_na_posicao <- 
    move(right).
    
+!explorar : pos(X,Y) & X == 6 & Y == 6 & not lixo_na_posicao <- 
    move(up).
    
+!explorar : pos(X,Y) & Y == 6 & X > 0 & not lixo_na_posicao <- 
    move(up).
    
+!explorar : pos(X,Y) & X == 0 & Y > 0 & not lixo_na_posicao <- 
    move(left).

// Verifica se ainda há lixos
+!verificar_lixos_restantes <- 
    .wait(1000);  // Espera incineração
    -lixo_depositado;
    ?lixo_na_posicao;
    !procurar_lixo.
    
+!verificar_lixos_restantes <- 
    .print("Todos os lixos foram coletados! Procurando moeda...");
    !procurar_moeda.

// Procura pela moeda
+!procurar_moeda <- 
    ?moeda_na_posicao;
    .print("Moeda encontrada! Coletando...");
    pick_moeda;
    .print("Moeda coletada! Missão concluída com sucesso!");
    !finalizar.
    
+!procurar_moeda <- 
    ?moeda_pos(X,Y);
    !navegar_para(X,Y);
    !procurar_moeda.

// Finalização
+!finalizar <- 
    .print("Programa finalizado.").