import jason.asSyntax.*;
import jason.environment.Environment;
import jason.environment.grid.GridWorldModel;
import jason.environment.grid.GridWorldView;
import jason.environment.grid.Location;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.util.Random;
import java.util.logging.Logger;

public class IncineratorRobotEnvironment extends Environment {

    public static final int GSize = 7;
    public static final int R1 = 0;
    public static final int R2 = 1;
    public static final int LIXO = 16;
    public static final int MOEDA = 32;

    static Logger logger = Logger.getLogger(IncineratorRobotEnvironment.class.getName());

    private GridWorldModel model;
    private GridWorldView view;

    @Override
    public void init(String[] args) {
        model = new GridWorldModel(GSize, GSize, 2);
        view = new GridWorldView(model, "Incinerator Robot", 600) {
            @Override
            public void draw(Graphics g, int x, int y, int object) {
                if (object == LIXO) {
                    drawLixo(g, x, y);
                } else if (object == MOEDA) {
                    drawMoeda(g, x, y);
                }
            }
            
            @Override
            public void drawAgent(Graphics g, int x, int y, Color c, int id) {
                if (id == R1) {
                    c = Color.BLUE;
                    g.setColor(c);
                    g.fillRect(x * cellSizeW + 2, y * cellSizeH + 2, cellSizeW - 4, cellSizeH - 4);
                    g.setColor(Color.WHITE);
                    g.setFont(new Font("Arial", Font.BOLD, 12));
                    g.drawString("R1", x * cellSizeW + 10, y * cellSizeH + 20);
                } else if (id == R2) {
                    c = Color.RED;
                    g.setColor(c);
                    g.fillOval(x * cellSizeW + 2, y * cellSizeH + 2, cellSizeW - 4, cellSizeH - 4);
                    g.setColor(Color.WHITE);
                    g.setFont(new Font("Arial", Font.BOLD, 12));
                    g.drawString("R2", x * cellSizeW + 10, y * cellSizeH + 20);
                }
            }
            
            public void drawLixo(Graphics g, int x, int y) {
                g.setColor(Color.GREEN);
                g.fillRect(x * cellSizeW + 8, y * cellSizeH + 8, cellSizeW - 16, cellSizeH - 16);
                g.setColor(Color.BLACK);
                g.drawString("L", x * cellSizeW + 15, y * cellSizeH + 25);
            }
            
            public void drawMoeda(Graphics g, int x, int y) {
                g.setColor(Color.YELLOW);
                g.fillOval(x * cellSizeW + 8, y * cellSizeH + 8, cellSizeW - 16, cellSizeH - 16);
                g.setColor(Color.BLACK);
                g.drawString("$", x * cellSizeW + 15, y * cellSizeH + 25);
            }
        };
        
        model.setAgPos(R1, 0, 0);
        model.setAgPos(R2, 3, 3);
        
        // Adiciona lixos
        model.add(LIXO, 1, 2);
        model.add(LIXO, 3, 5);
        model.add(LIXO, 4, 4);
        model.add(LIXO, 6, 6);
        
        // Adiciona moeda
        model.add(MOEDA, 4, 5);
        
        updatePercepts();
    }

    @Override
    public boolean executeAction(String agName, Structure action) {
        boolean result = false;
        
        try {
            if (agName.equals("R1")) {
                if (action.getFunctor().equals("move")) {
                    String direction = action.getTerm(0).toString();
                    result = moveR1(direction);
                } else if (action.getFunctor().equals("pick_lixo")) {
                    result = pickLixo();
                } else if (action.getFunctor().equals("drop_lixo")) {
                    result = dropLixo();
                } else if (action.getFunctor().equals("pick_moeda")) {
                    result = pickMoeda();
                }
            } else if (agName.equals("R2")) {
                if (action.getFunctor().equals("incinerate")) {
                    result = incinerateLixo();
                }
            }
            
            if (result) {
                updatePercepts();
                Thread.sleep(200);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return result;
    }
    
    private boolean moveR1(String direction) {
        Location r1 = model.getAgPos(R1);
        int x = r1.x, y = r1.y;
        
        switch (direction) {
            case "up": if (y > 0) y--; break;
            case "down": if (y < GSize-1) y++; break;
            case "left": if (x > 0) x--; break;
            case "right": if (x < GSize-1) x++; break;
        }
        
        if (model.isFree(x, y)) {
            model.setAgPos(R1, x, y);
            informAgsEnvironmentChanged();
            return true;
        }
        return false;
    }
    
    private boolean pickLixo() {
        Location r1 = model.getAgPos(R1);
        if (model.hasObject(LIXO, r1)) {
            model.remove(LIXO, r1);
            return true;
        }
        return false;
    }
    
    private boolean dropLixo() {
        Location r1 = model.getAgPos(R1);
        if (!model.hasObject(LIXO, r1)) {
            model.add(LIXO, r1);
            return true;
        }
        return false;
    }
    
    private boolean pickMoeda() {
        Location r1 = model.getAgPos(R1);
        if (model.hasObject(MOEDA, r1)) {
            model.remove(MOEDA, r1);
            return true;
        }
        return false;
    }
    
    private boolean incinerateLixo() {
        Location r2 = model.getAgPos(R2);
        if (model.hasObject(LIXO, r2)) {
            model.remove(LIXO, r2);
            return true;
        }
        return false;
    }

    private void updatePercepts() {
        clearPercepts("R1");
        clearPercepts("R2");
        
        Location r1 = model.getAgPos(R1);
        Location r2 = model.getAgPos(R2);
        
        // Percepts para R1
        addPercept("R1", Literal.parseLiteral("pos(" + r1.x + "," + r1.y + ")"));
        addPercept("R1", Literal.parseLiteral("r2_pos(" + r2.x + "," + r2.y + ")"));
        
        // Verifica se há lixo na posição atual
        if (model.hasObject(LIXO, r1)) {
            addPercept("R1", Literal.parseLiteral("lixo_na_posicao"));
        }
        
        // Verifica se há moeda na posição atual
        if (model.hasObject(MOEDA, r1)) {
            addPercept("R1", Literal.parseLiteral("moeda_na_posicao"));
        }
        
        // Verifica se está na posição do R2
        if (r1.x == r2.x && r1.y == r2.y) {
            addPercept("R1", Literal.parseLiteral("no_incinerador"));
        }
        
        // Percepts para R2
        addPercept("R2", Literal.parseLiteral("pos(" + r2.x + "," + r2.y + ")"));
        
        // Verifica se há lixo para incinerar
        if (model.hasObject(LIXO, r2)) {
            addPercept("R2", Literal.parseLiteral("lixo_para_incinerar"));
        }
        
        informAgsEnvironmentChanged();
    }
}