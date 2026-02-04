#include <string>
#include <iostream>
#include <vector>
#include <map>
#include <random>

// datos: tamaño del lado del tablero, simbolo del jugador, coordenadas del jugador.
int size_alto = 7;
int size_ancho = 12;

// var global statica que lleva el control del num de enemies
static int enemies_created = 0;

// funcion de limpieza completa del buffer
void buffer_cleaner(void) {
    int c;
    // obtenemos un char del buffer siempre y cuando no sea un salto de linea o el final de un archivo
    while ((c = getchar()) != 10 && c != EOF);
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
std::vector<std::string> map_board(void) {
    std::vector<std::string> board;
    // crear tablero el bucle exterior controla el numero de filas y el interior los caracteres por fila
    for (int i=1; i <= size_alto; i++) {
        for (int j=1; j <= size_ancho; j++) {
            if (!(i == 1 || i == size_alto || j == 1 || j == size_ancho)) board.push_back(".");
            else board.push_back("#");
        }
    }
    return board;
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
        // si la entidad no es player comparamos
        if (!(entidad == "player")) {
            // revisamos si las player_x_y son iguales a alguna entities_x_y y si son iguales retornamos false
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

// funcion de creacion del tablero revisando coordenadas
bool map_entities_x_y(
    const std::vector<std::vector<int>>& board_x_y,
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities
)
{
    // declaramos var de control del personaje y le damos el valor true
    bool vivo = true;
    // limites
    int lim_borde_inferior = size_alto-1;
    int lim_borde_derecho = size_ancho-1;
    // bucle para asignar las posiciones de las entidades_x_y iterando sobre la lista de board_x_y
    for (int i=0; i < board_x_y.size(); i++) {
        // recorremos diccionario para obtener las coordenadas de las entidades
        for (auto& [entidad, data] : entities) {
            // condicionales que revisan que la entidad_x_y exista en las board_x_y y que no este en algun limite
            // condicional que revisa si las player_x_y conciden con alguna casilla
            if (entities[entidad].x == board_x_y[i][0] && entities[entidad].y == board_x_y[i][1]) {
                // condicional que actualiza player si player_i no son las misma coordenadas que las de limite
                if (!(board_x_y[i][0] == 0 || board_x_y[i][1] == 0 || board_x_y[i][0] == lim_borde_derecho || board_x_y[i][1] == lim_borde_inferior)) {
                    entities[entidad].indice = i;
                    // como no hubo errores actualizamos la var de control del ultimo movimiento del player
                    last_move_entities[entidad].x = entities[entidad].x;
                    last_move_entities[entidad].y = entities[entidad].y;
                    // funcion para revisar si las coordenadas de enemigo concuerda con la del player devuelve false si concuerdan y true si no
                    vivo = player_colE(entities, board_x_y);
                    // revisamos si el valor es false
                    if (!vivo) {
                        // cambiamos simbolo de personaje por una x
                        entities["player"].symbol = 'x';
                        return vivo;
                    }
                }
                // si las player_x_y son las mismas que las de un limite no actualizamos player
                // igual restablecemos las player_x_y a su ultimo movimiento usando una var de control para que se pueda mover, de nuevo
                else {
                    entities[entidad].x = last_move_entities[entidad].x;
                    entities[entidad].y = last_move_entities[entidad].y;
                }
            }
        }
    }
    return vivo;
}

// funcion de creacion del tablero revisando coordenadas
std::string board_creator(
    const std::vector<std::string>& board,
    std::map<std::string, Entity>& entities
)
{
    std::string board_view;
    // creamos var de control donde controlamos el numero de chars por fila y usar salto de linea
    int field_length = 1;
    // bucle para crear el tablero iterando sobre la lista de caracteres que conforma nuestro tablero
    for (int i=0; i < board.size(); i++) {
        // var de control para saber si hubo concidencia de indices con entidades con la casilla que iteramos
        bool not_entity = true;
        // bucle para iterar sobre nuestro dicts de entidades y revisar si conincide con alguna casilla
        for (auto& [entidad, data] : entities) {
            // si el indice de la entidad coincide con el de la casilla agregamos simbolo al tablero en vez de la casilla
            if (entities[entidad].indice == i) {
                board_view += entities[entidad].symbol;
                // var de control que ponemos en false porque si hubo entity en la casilla
                not_entity = false;
                // salimos del bucle en la primera coincidencia
                break;
            }
        }
        // revisamos si la var de control es true, osea no hubo entidad y si es cierto agregamos casilla normal
        if (not_entity) board_view += board[i];
        // revisar si la var de control ya es la igual a la longitud del lado del size_map y si es true añadir salto de linea y reiniciar var
        if (field_length == size_ancho) {
            board_view += "\n";
            field_length = 0;
        }
        // añadir uno a nuestra var de control para actualizar que agregamos un caracter mas a la fila
        field_length++;
    }
    return board_view;
}

// funcion para preguntar si quiere seguir jugando
bool continue_game(void) {
    char continuar;
    // preguntamos y guardamos respuesta en variable
    printf("Quiere dejar de jugar? (s/n): "); scanf(" %c", &continuar);
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

void insert_enemies_dicts(
    std::map<std::string, Entity>& entities,
    std::map<std::string, last_move_Entity>& last_move_entities,
    std::string clave,
    int casilla_x,
    int casilla_y
)
{
    // agregar el nuevo enemigo al diccionario de entities y al de el last_move_entities
    entities.insert({clave, {'E', casilla_x, casilla_y, 0}});
    last_move_entities.insert({clave, {casilla_x, casilla_y}});
    // aumentamos en 1 el num_enemy para indicar que ya se creo uno nuevo
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
        if (!(entidad == "player")) {
            // generar numero aleatorio entre 0 y el rango especificado
            int direccion = distrib(gen);
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
                default:
                    printf("Checa los rangos de la distribucion");
                    break;
            }
        }
    }
    return 0;
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
            if (!(casilla_x == 0 || casilla_y == 0 || casilla_x == lim_borde_derecho || casilla_y == lim_borde_inferior)) {
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
                    insert_enemies_dicts(entities, last_move_entities, clave, casilla_x, casilla_y);
                    // sumamos 1 a la var global que controla el de num_enemy
                    enemies_created++;
                    break;
                }
            }
        }
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
    // llamamos funcion que reinicie las entidades
    dicts_entities(entities, last_move_entities);
    // llamamos funcion para que cree a los enemigos
    creating_enemies(board_x_y, entities, last_move_entities, cant_enemies);
}

void creating_point(
    std::map<std::string, Entity>& entities,
    std::vector<std::vector<int>>& board_x_y
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
            entities.insert({"point", {'+', casilla_x, casilla_y, 0}});
            break;
        }
    }
}

int main(void) {
    // vars que controlas la repeticion del juego
    bool play = true;
    // crear diccionario de entidades, su indentificador sera el tipo de entidad y los datos seran la plantilla de la estructura Entity
    std::map<std::string, Entity> entities;
    // crear diccionario de ultima direccion_x_y de las entidades
    std::map<std::string, last_move_Entity> last_move_entities;
    // llamamos funcion para declarar valores predetermidos de sus diccionarios
    dicts_entities(entities, last_move_entities);

    // llamamos funcion de mapeo del tablero y de mapeo de board_x_y para obtener las casillas y sus coordenadas
    std::vector<std::string> board = map_board();
    std::vector<std::vector<int>> board_x_y = map_board_x_y();

    // llamamos la funcion para crear 6 primeros enemigos
    creating_enemies(board_x_y, entities, last_move_entities, 4);

    // creamos punto inicial
    creating_point(entities, board_x_y);

    // ideas para añadir, antes de limpiar buffer revisar longitu para evitar procesar numeros masivos


    // zona de debug, para mostrar outputs

    // bucle principal donde se repetira el juego en el cual se actualizara cada vez el tablero
    printf("Muevete: w = up, s = down, d = right, a = left\n\n");
    while (play) {
        // reinicio vars control para la var de control del while loop
        bool play_again = true, reset = false;

        // aplicamos funcion movimientos random de los enemigos
        random_movements(entities, 3, false);

        // llamamos funcion de parse de coordenadas y lo guardamos en una variable
        bool map_entities = map_entities_x_y(board_x_y, entities, last_move_entities);

        // revisamos que el jugador no haya muerto
        if (!map_entities) {
            std::cout << board_creator(board, entities);
            printf("MORISTE\n");
            // llamamos funcion que revisa las respuesta del usuario y guarda el rdo en la var que controla el while loop
            play_again = continue_game();
            reset = play_again;
        }
        // si no murio continuamos el juego
        else {
            // mostramos tablero actualizado
            std::cout << board_creator(board, entities);
            // pedimos input del movimieto que el jugador quiera hacer w = up, s = down, d = right, l = left
            char posicion; scanf(" %c", &posicion);
            // actualizamos player_x_y segun la posicion a la cual el usuario se dirija usando switch
            switch (posicion) {
                // dentro cada case usamos la funcion buffer_cleaner para mantener movimiento a una casilla
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
                    play_again = continue_game();
                    break;
            }
        }
        // revisamos si quit_playing es true y si es salimosss
        if (!play_again) {
            break;
        }
        // revisamos si play_again es true y si es reseteamos tablero y entidades
        if (play_again && reset) {
            reset_game(board_x_y, entities, last_move_entities, 4);
            continue;
        }
    }
}
