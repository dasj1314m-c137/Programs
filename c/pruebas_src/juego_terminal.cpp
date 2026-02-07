#include <string>
#include <iostream>
#include <vector>
#include <map>
#include <random>
#include <ncurses.h>

// datos: tamaño del lado del tablero, simbolo del jugador, coordenadas del jugador.
int size_alto = 7;
int size_ancho = 14;

// var global estatica que lleva el control del num de enemies
static int enemies_created = 0;
// var global estatica que lleva el control de la cant de puntos
static int cant_puntos = 0;
static int pts_for_enemy = 0;


std::pair<int, int> AlignCenter(int x, int y) {
    int filas, columnas;
    getmaxyx(stdscr, filas, columnas);
    int offset_x = (columnas - size_ancho - 15) / 2;
    int offset_y = (filas - size_alto) / 2;

    return {offset_x + x, offset_y + y};
}

std::pair<int, int> Align_pts(void) {
    static std::pair<int, int> center_x_y = AlignCenter(0, 0);
    static int offset_y = center_x_y.second - 2;
    return {center_x_y.first, offset_y};
}

std::pair<int, int> Align_msj(void) {
    static std::pair<int, int> center_x_y = AlignCenter(0, 0);
    static int offset_y = center_x_y.second + size_alto + 2;
    return {center_x_y.first, offset_y};
}

// funcion de limpieza completa del buffer
void buffer_cleaner(void) {
    flushinp();
}

// crear structura de datos para mis entidades con sus simbolos y coordenadas y tambien para sus ultimos movimientos
struct Entity {
    char symbol;
    int x, y;
    int indice;
};

struct last_move_Entity {
    int x, y;
};

// funcion de mapeo de coordenadas del tablero
std::vector<std::vector<int>> map_board_x_y(void) {
    std::vector<std::vector<int>> board_x_y;
    // bucle anidado el bucle exterior controlara la coordenada 'y' y el interior la 'x' llendo fila por fila creando sus coordenadas
    for (int y=0; y < size_alto; y++) {
        for (int x=0; x < size_ancho; x++) {
            board_x_y.push_back({x, y});
        }
    }
    return board_x_y;
}

// funcion que recibe el tamaño del tablero y crea un cuadrado con bordes de '#' y las casillas '.' y regresa el tablero en string
std::vector<char> map_board(void) {
    std::vector<char> board;
    // crear tablero el bucle exterior controla el numero de filas y el interior los caracteres por fila
    for (int i=1; i <= size_alto; i++) {
        for (int j=1; j <= size_ancho; j++) {
            if (!(i == 1 || i == size_alto || j == 1 || j == size_ancho)) board.push_back('.');
            else board.push_back('#');
        }
    }
    return board;
}

// funcion para determinar movimientos aleatorios y apariciones de entidades usando sus x_y
int random_movements(
    std::map<std::string, Entity>& entities,
    int max_range,
    bool aparicion
) {
    // preparando datos para obtencion de numeros aleatorios
    static std::random_device rd;
    static std::mt19937 gen(rd());
    // recibimos un rango maximo y siempre el rango minimo es 0
    std::uniform_int_distribution<> distrib(0, max_range);

    // si aparicion es true generar numero aleatorio entre 0 y el rango especificado y retornarlo
    if (aparicion) return distrib(gen);

    // recorremos nuestras entidades para poder obtener sus valor y claves
    for (auto& [entidad, data] : entities) {
        // solo aplicar movimientos aleatorios a entidades que no sean el player
        if (entidad != "player" && entidad != "point") {
            // bucle while para evitar mover enemigo en la misma posicion que otro enemigo
            while (true) {
                // var de control para saber si la casilla esta libre por defecto en true
                bool casilla_libre = true;
                // generar numero aleatorio entre 0 y el rango especificado
                int direccion = distrib(gen);
                // vars para saber el ultimo movimiento de la entidad y poder reinciarlas si hace falta
                int last_posX = entities[entidad].x;
                int last_posY = entities[entidad].y;
                // dependiendo del numero sumamos o restamos a las x_y para cambiar su posicion en 1 coordenada
                switch (direccion) {
                    case 0:
                        entities[entidad].x += 1;
                        break;
                    case 1:
                        entities[entidad].y -= 1;
                        break;
                    case 2:
                        entities[entidad].x -= 1;
                        break;
                    case 3:
                        entities[entidad].y += 1;
                        break;
                    case 4:
                        break;
                }
                // recorrer nuestro dict de entidades para comparar la nueva posicion de la entidad con las demas entidades
                for (auto& [entity, datos] : entities) {
                    // revisar que la entidad a comparar no sea el player ni el mismo ni el punto
                    if (entity != "player" && entity != entidad) {
                        // si las coordenadas del movimiento concuerdan con otra entidad
                        if (entities[entidad].x == entities[entity].x && entities[entidad].y == entities[entity].y) {
                            // ponemos casilla libre en false
                            casilla_libre = false;
                            break;
                        }
                    }
                }
                // si la casilla libre salimos del bucle while y seguimos con la siguiente entidad
                if (casilla_libre) break;
                // si la casilla no esta libre reiniciamos las entities_x_y a sus ultimos que tuvo antes del cambio
                entities[entidad].x = last_posX;
                entities[entidad].y = last_posY;
            }
        }
    }
    return 0;
}

void creating_point(
    std::map<std::string, Entity>& entities,
    const std::vector<std::vector<int>>& board_x_y
)
{
    // maximo indice para poder obtener un indice aleatorio
    int max_i = board_x_y.size() - 1;
    // limites
    int lim_borde_inferior = size_alto-1;
    int lim_borde_derecho = size_ancho-1;
    // bucle while hasta que casilla_x_y sea valida y creamos nuestra entidad point
    while (true) {
        // var de control para saber si la casilla esta libre por defecto true
        bool casilla_libre = true;
        // obtener indice aleatorio para obtener coordenadas de board_x_y
        int i = random_movements(entities, max_i, true);
        // obtener la casilla_x_y usando el indice de board_x_y
        int casilla_x = board_x_y[i][0];
        int casilla_y = board_x_y[i][1];
        // revisar si las casilla_x_y son limites y en ese caso no continuar o continuar con el bucle redundante de nuevo el bucle
        if (casilla_x == 0 || casilla_y == 0 || casilla_x == lim_borde_derecho || casilla_y == lim_borde_inferior) continue;
        // si no son limites como checamos arriba recorrer la lista de entidades
        for (auto& [entidad, data] : entities) {
            // revisar si la casilla_x_y concuerda con alguna entity_x_y
            if (casilla_x == entities[entidad].x && casilla_y == entities[entidad].y) {
                // si concuerda cambiamos nuestra var de control a false porque la casilla esta ocupada y salimos en la primera coincidencia
                casilla_libre = false;
                break;
            }
        }
        // si casilla libre es true creamos nuestra entidad point y salimos del bucle while
        if (casilla_libre) {
            // creamos la entidad point y el indice se lo pasamos a este porque cuando la creamos de nuevo el indice ya se parse para las demas entidades
            entities.insert({"point", {'+', casilla_x, casilla_y, i}});
            break;
        }
    }
}

// funcion que revisa si alguna coordenada del jugador coincide con la de un enemigo
bool player_colE(
    std::map<std::string, Entity>& entities,
    const std::vector<std::vector<int>>& board_x_y
)
{
    // var de control por defecto vacio osea ningun match de player_x_y y enemy_x_y
    std::string enemigo_borrar = "";
    // recorrer diccionario de entidades
    for (auto& [entidad, data] : entities) {
        // si la entidad no es player y si no es point comparamos
        if ((entidad != "player" && entidad != "point")) {
            // revisamos si las player_x_y son iguales a alguna entities_x_y
            if (entities["player"].x == entities[entidad].x && entities["player"].y == entities[entidad].y) {
                // recorrer board_x_y para encontrar el indice del encuentro de las coordenadas de la entidad y el player
                for (int i=0; i < board_x_y.size(); i++) {
                    // revisamos que las coordenadas del player coincidad con alguna casilla
                    if (entities["player"].x == board_x_y[i][0] && entities["player"].y == board_x_y[i][1]) {
                        // al encontrar la casilla igual tomamo el indice y se lo pasamos al player
                        entities["player"].indice = i;
                        break;
                    }
                }
                // guardamos en una var la entidad a borrar, para no dejar iteradores que apunta al vacio
                enemigo_borrar = entidad;
                break;
            }
        }
    }
    // revisamos si enemigo a borrar esta vacio osea nuestro player_x_y no hizo match con ningun enemy_x_y
    if (enemigo_borrar.empty()) return true;
    else {
        // eliminamos enemigo
        entities.erase(enemigo_borrar);
        return false;
    }
}

// funcion que revisa si alguna coordenada del jugador concuerda con al del point
void player_colP(
    std::map<std::string, Entity>& entities,
    const std::vector<std::vector<int>>& board_x_y
)
{
    // revisamos si el player_x_y son iguales al point_x_y
    if (entities["player"].x == entities["point"].x && entities["player"].y == entities["point"].y) {
        // si la condicion se cumple eliminamos point
        entities.erase("point");
        cant_puntos++;
        pts_for_enemy++;
        // luego de eliminar el antiguo point creamos otro nuevo
        creating_point(entities, board_x_y);
    }
}

void insert_enemies_dicts(
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities,
    std::string clave,
    int casilla_x,
    int casilla_y,
    int indice
)
{
    // agregar el nuevo enemigo al diccionario de entities y al de el last_move_entities
    entities.insert({clave, {'E', casilla_x, casilla_y, indice}});
    last_move_entities.insert({clave, {casilla_x, casilla_y}});
    // aumentamos en 1 el num_enemy para indicar que ya se creo uno nuevo
}

void creating_enemies(
    std::vector<std::vector<int>>& board_x_y,
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities,
    int cant_enemies
)
{
    // var del maximo indice porque size devuelve cant no max_indice
    int max_i = board_x_y.size() - 1;
    for (int j=0; j < cant_enemies; j++) {
        // creamos la clave de nuestro enemigo
        std::string clave = "enemy_" + std::to_string(enemies_created);
        // limites
        int lim_borde_inferior = size_alto-1;
        int lim_borde_derecho = size_ancho-1;
        // iteramos hasta que obtengamos una coordenada valida
        while (true) {
            // var de control que revisa si la casilla esta libre por defecto es true
            bool casilla_libre = true;
            // obtener indice aleatorio de las board_x_y para posicionar nuestro enemigo
            int i = random_movements(entities, max_i, true);
            // guardamos la casilla_x_y en vars para comparacion mas facil
            int casilla_x = board_x_y[i][0];
            int casilla_y = board_x_y[i][1];
            // revisar que la coordenada no sea un limite
            if (casilla_x == 0 || casilla_y == 0 || casilla_x == lim_borde_derecho || casilla_y == lim_borde_inferior) continue;
            // iteramos el diccionario de entidades
            for (auto& [entidad, data] : entities) {
                // compara si las coordenadas son igual a otra entidad
                bool x_y_inEntidad = (entities[entidad].x == casilla_x && entities[entidad].y == casilla_y);
                if (x_y_inEntidad) {
                    casilla_libre = false;
                            break;
                }
            }
            // si la casilla esta libre agregamos al enemigo
            if (casilla_libre) {
                insert_enemies_dicts(entities, last_move_entities, clave, casilla_x, casilla_y, i);
                // sumamos 1 a la var global que controla el de num_enemy
                enemies_created++;
                break;
            }
        }
    }
}


void aparicion_enemies(
    std::vector<std::vector<int>>& board_x_y,
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities
)
{
    if (pts_for_enemy != 0 && pts_for_enemy % 3 == 0) {
        creating_enemies(board_x_y, entities, last_move_entities, 1);
        pts_for_enemy = 0;
    }
}

// funcion de creacion del tablero revisando coordenadas
bool map_entities_x_y(
    const std::vector<std::vector<int>>& board_x_y,
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities
)
{
    // declaramos vars de control del personaje y le damos el valor true
    bool vivo = true;
    // limites
    int lim_borde_inferior = size_alto-1;
    int lim_borde_derecho = size_ancho-1;
    // bucle para asignar las posiciones de las entidades_x_y iterando sobre la lista de board_x_y
    for (int i=0; i < board_x_y.size(); i++) {
        // recorremos diccionario para obtener las coordenadas de las entidades
        for (auto& [entidad, data] : entities) {
            // condicionales que revisan que la entidad_x_y exista en las board_x_y y que no este en algun limite
            // condicional que revisa si las entities conciden con alguna casilla
            if (entities[entidad].x == board_x_y[i][0] && entities[entidad].y == board_x_y[i][1]) {
                // condicional que actualiza player si player_i no son las misma coordenadas que las de limite
                if (!(board_x_y[i][0] == 0 || board_x_y[i][1] == 0 || board_x_y[i][0] == lim_borde_derecho || board_x_y[i][1] == lim_borde_inferior)) {
                    entities[entidad].indice = i;
                    // !!!!revisar que la entidad no sea point porque esta entidad no tiene last_move
                    if (entidad != "point") {
                        // como no hubo errores actualizamos la var de control del ultimo movimiento de la entidad
                        last_move_entities[entidad].x = entities[entidad].x;
                        last_move_entities[entidad].y = entities[entidad].y;
                    }
                }
                // si las player_x_y son las mismas que las de un limite no actualizamos player
                // igual restablecemos las player_x_y a su ultimo movimiento usando una var de control para que se pueda mover, de nuevo
                else {
                    // !!!!revisar que la entidad no sea point porque esta entidad no tiene last_move
                    if (entidad != "point") {
                        entities[entidad].x = last_move_entities[entidad].x;
                        entities[entidad].y = last_move_entities[entidad].y;
                    }
                }
            }
        }
    }
    // funcion para revisar si las coordenadas de enemigo concuerda con la del player devuelve false si concuerdan y true si no
    vivo = player_colE(entities, board_x_y);
    // revisamos si el valor es false
    if (!vivo) {
        // cambiamos simbolo de personaje por una x
        entities["player"].symbol = 'x';
        return vivo;
    }
    // funcion para revisar si las player_x_y son iguales a las de point_x_y
    player_colP(entities, board_x_y);
    return vivo;
}

void addChar_VS(int& x, int& y, char& simbolo) {
    mvaddch(y, x, simbolo);
}

// funcion de creacion del tablero revisando coordenadas
void board_creator(
    std::vector<char>& board,
    std::vector<std::vector<int>>& board_x_y,
    std::map<std::string, Entity>& entities
)
{
    // limpiamos pantalla virtual
    clear();
    // recorremos board_x_y para obtener x_y y mediante el contador obtener simbolo
    for (int i=0; i < board_x_y.size(); i++) {
        // llamar a funcion para añadir offset hacia el centro
        std::pair<int, int> center_x_y = AlignCenter(board_x_y[i][0], board_x_y[i][1]);
        addChar_VS(center_x_y.first, center_x_y.second, board[i]);
    }
    // recorremos entities para obtener sus x_y y tambien su simbolo
    for (auto& [entidad, data] : entities) {
        // aplicamos zoom a las entidades
        std::pair<int, int> center_x_y = AlignCenter(entities[entidad].x, entities[entidad].y);
        addChar_VS(center_x_y.first, center_x_y.second, entities[entidad].symbol);
    }
}

// funcion para preguntar si quiere seguir jugando
bool continue_game(int& x, int& y) {
    // preguntamos y guardamos respuesta en variable
    mvprintw(y, x, "Quiere dejar de jugar? (s/n): ");
    refresh();
    char continuar = getch();
    // comparamos el input y si es 's' play_again igual a true en cambio false
    switch (continuar) {
        case 'n':
            return true;
            break;
        default:
            return false;
            break;
    }
}

// funcion que declara los valores de los diccionarios de entidades y sus ultimos movimientos
void dicts_entities(
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities
)
{
    entities = {
        {"player", {'@', 1, 1, 0}}
    };
    last_move_entities = {
        {"player", {1, 1}}
    };
}

void delete_enemies_dicts(
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities
)
{
    for (int i=0; i < enemies_created; i++) {
        std::string clave = "enemy_" + std::to_string(i);
        entities.erase(clave);
        last_move_entities.erase(clave);
    }
}

void reset_game(
    std::vector<std::vector<int>>& board_x_y,
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities,
    int cant_enemies
)
{
    // llamamos funcion para que elimine los enemigos de los dicts
    delete_enemies_dicts(entities, last_move_entities);
    // resetear var de control del numero de enemigos
    enemies_created = 0;
    // resetear var de contador de nuestros puntos
    cant_puntos = 0;
    // resetear var de control para crear enemies segun puntos
    pts_for_enemy = 0;
    // llamamos funcion que reinicie las entidades
    dicts_entities(entities, last_move_entities);
    // llamamos funcion para que cree a los enemigos
    creating_enemies(board_x_y, entities, last_move_entities, cant_enemies);
    // funcion para crear la entidad point
    creating_point(entities, board_x_y);
}

int main(void) {
    // incializar ncurses
    initscr();
    // evitamos que las letras que el usuario escriba se impriman
    noecho();
    // permitimos leer letras indmediatamente sin ingresar ENTER
    cbreak();
    // ocultamos el cursos poniendo
    curs_set(0);
    // habilitamos teclas especiales para evitar errores por si son ingresadas
    keypad(stdscr, TRUE);
    // vars que controlas la repeticion del juego
    bool play = true;
    // crear diccionario de entidades, su indentificador sera el tipo de entidad y los datos seran la plantilla de la estructura Entity
    std::map<std::string, Entity> entities;
    // crear diccionario de ultima direccion_x_y de las entidades
    std::map<std::string, last_move_Entity> last_move_entities;
    // llamamos funcion para declarar valores predetermidos de sus diccionarios
    dicts_entities(entities, last_move_entities);

    // llamamos funcion de mapeo del tablero y de mapeo de board_x_y para obtener las casillas y sus coordenadas
    std::vector<char> board = map_board();
    std::vector<std::vector<int>> board_x_y = map_board_x_y();

    // llamamos la funcion para crear 6 primeros enemigos
    creating_enemies(board_x_y, entities, last_move_entities, 3);

    // creamos punto inicial
    creating_point(entities, board_x_y);

    // obtener coordendas para los mensajes y para la UI
    static std::pair<int, int> pts_x_y = Align_pts();
    static std::pair<int, int> msj_x_y = Align_msj();

    // ideas para añadir, antes de limpiar buffer revisar longitu para evitar procesar numeros masivos
    // zona de debug, para mostrar outputs

    // bucle principal donde se repetira el juego en el cual se actualizara cada vez el tablero
    while (play) {
        // reinicio vars control para la var de control del while loop
        bool play_again = true, reset = false;

        // llamamos funcion de parse de coordenadas y lo guardamos en una variable
        bool map_entities = map_entities_x_y(board_x_y, entities, last_move_entities);

        // creamos tablero virtual
        board_creator(board, board_x_y, entities);

        // mostrar puntos totales del jugador
        mvprintw(pts_x_y.second, pts_x_y.first, "Puntos: %d", cant_puntos);

        // revisamos que el jugador no haya muerto
        if (!map_entities) {
            mvprintw(msj_x_y.second, msj_x_y.first, "MORISTE");
            refresh();
            // llamamos funcion que revisa las respuesta del usuario y guarda el rdo en la var que controla el while loop
            play_again = continue_game(msj_x_y.first, msj_x_y.second);
            reset = play_again;
        }
        // si no murio continuamos el juego
        else {
            // mostramos tablero actualizado
            refresh();
            // pedimos input del movimieto que el jugador quiera hacer w = up, s = down, d = right, l = left
            char posicion = getch();
            // actualizamos player_x_y segun la posicion a la cual el usuario se dirija usando switch
            switch (posicion) {
                // dentro cada case usamos la funcion buffer_cleaner para mantener movimiento a una casilla
                /*!!!!!
                * MOVIMIENTO CON ROLLBACK (HOBBY / PROTOTIPO)
                *
                * Actualmente las entidades se mueven primero y luego se valida su posición.
                * Si la posición es inválida, se restaura la coordenada anterior desde
                * `last_moves_entities`.
                *
                * ⚠️ IMPORTANTE:
                * Este enfoque funciona para prototipos, pero NO escala bien.
                * Si el juego crece (más reglas, efectos, IA, animaciones, eventos),
                * este sistema puede causar bugs sutiles y estados inconsistentes.
                *
                * FUTURO (SI SE ESCALA):
                * - Cambiar a modelo de "intención de movimiento":
                *   input → intención (dx, dy) → validación → aplicar movimiento
                * - Evitar rollback como mecanismo principal.
                */
                case 'w':
                    entities["player"].y -= 1;
                    buffer_cleaner();
                    break;
                case 's':
                    entities["player"].y += 1;
                    buffer_cleaner();
                    break;
                case 'd':
                    entities["player"].x += 1;
                    buffer_cleaner();
                    break;
                case 'a':
                    entities["player"].x -= 1;
                    buffer_cleaner();
                    break;
                // si ingresa otra opcion preguntar si quiere salir del juego
                default:
                    // llamamos funcion que revisa las respuesta del usuario y guarda el rdo en la var que controla el while loop
                    play_again = continue_game(msj_x_y.first, msj_x_y.second);
                    break;
            }
        }
        // revisamos si el jugador alcanzo cierta cantidad de puntos y le felicitamos por su victoria
        if (cant_puntos == 25) {
            mvprintw(msj_x_y.second, msj_x_y.first, "GANASTE");
            refresh();
            // preguntamos si quiere jugar de nuevo
            play_again = continue_game(msj_x_y.first, msj_x_y.second);
            reset = play_again;
        }
        // revisamos si play_again es true y si es salimosss
        if (!play_again) {
            endwin();
            break;
        }
        // revisamos si play_again es true y si es reseteamos tablero y entidades
        if (play_again && reset) {
            reset_game(board_x_y, entities, last_move_entities, 3);
            continue;
        }

        // aplicamos funcion movimientos random de los enemigos
        random_movements(entities, 4, false);

        // llamamos funcion de aparicion de enemies
        aparicion_enemies(board_x_y, entities, last_move_entities);
    }
}
