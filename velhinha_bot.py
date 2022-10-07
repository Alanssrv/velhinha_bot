import telebot
import re
import time
import jogo_velha

theBoard = [' '] * 10
playerLetter, computerLetter = ['X', 'O']
isPlayer = False
gameIsPlaying = False

bot = telebot.TeleBot("TOKEN", parse_mode = None)

@bot.message_handler(commands=['start', 'menu'])
def command_start(message):
    clear_params()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/jogo_da_velha', '/como_jogar')
    start_markup.row('/sobre', '/jogar')
    bot.send_message(message.chat.id, "👵🏽 Olá, eu sou a Velhinha, sou um bot que te desafia no jogo da velha!\nClique em /sobre para mais de mim", reply_markup=start_markup)
    bot.send_message(message.chat.id, "O que é o /jogo_da_velha?\nQuer saber /como_jogar com a velhinha?")
    bot.send_message(message.chat.id, "Para iniciar uma partida contra a Velhinha, clique em /jogar")
    

@bot.message_handler(commands=['jogo_da_velha'])
def help(message):
    clear_params()
    bot.send_message(message.chat.id, "O jogo da velha ou jogo do galo ou três em linha é um jogo e/ou passatempo popular.\nÉ um jogo de regras extremamente simples, que não traz grandes dificuldades para seus jogadores e é facilmente aprendido.")
    bot.send_message(message.chat.id, "No modo básico do jogo, participam duas pessoas, que jogam alternadamente, preenchendo cada um dos\nespaços vazios. Cada participante poderá usar um símbolo (❌ ou ⭕). Vence o jogador que conseguir formar primeiro uma linha com três símbolos iguais, seja ela na horizontal, vertical ou diagonal.")
    

@bot.message_handler(commands=['sobre'])
def about(message):
    clear_params()
    bot.send_message(message.chat.id, "Eu sou a Velhinha, uma IA desenvolvida para te desafiar no Jogo da Velha, minha especialidade.\nFui desenvolvida com @BotFather e Python 🐍, por @alanssrv",)


@bot.message_handler(commands=['como_jogar'])
def how_play(message):
    clear_params()
    bot.send_message(message.chat.id, "Você sempre jogar com o ❌ e a velhina com a ⭕, antes de iniciar a partida você pode escolher quem a inicia jogando")
    bot.send_message(message.chat.id, "Para jogar, selecione um número de 1 a 9 que corresponde a cada posição da malha, ordenadas de baixo para cima, iniciando da direita inferior")
    bot.send_message(message.chat.id, "Para facilitar o teclado rápido do Telegram está com as posições das casas já organizadas com cada número")


@bot.message_handler(commands=['jogar'])
def change_player(message):
    clear_params()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/eu', '/vc')
    bot.send_message(message.chat.id, "Escolha quem começa jogando\n/eu ❌\n/vc (a Velhinha) ⭕", reply_markup=start_markup)

def clear_params():
    global theBoard
    global isPlayer
    global gameIsPlaying
    theBoard = [' '] * 10
    isPlayer = False
    gameIsPlaying = False

def desenha(message):
    global theBoard
    space = "   "
    position = ['◻'] * 10
    for index in range(10):
        if theBoard[index] == 'X':
            position[index] = '❌'
        if theBoard[index] == 'O':
            position[index] = '⭕'
    msg = position[7] + space + position[8] + space + position[9] + '\n\n'
    msg += position[4] + space + position[5] + space + position[6] + '\n\n'
    msg += position[1] + space + position[2] + space + position[3]
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda m: re.search(r'^[1-9]$', m.text))
def player_move(message):
    global theBoard
    global playerLetter, computerLetter
    global isPlayer
    global gameIsPlaying

    time.sleep(2)
    move = int(message.text)
    if theBoard[move] != ' ':
        bot.send_message(message.chat.id, "Posição já ocupada\nEscolha uma nova posição")
        return

    if gameIsPlaying:
        if isPlayer:
            jogo_velha.makeMove(theBoard, playerLetter, move)
            desenha(message)
            if jogo_velha.isWinner(theBoard, playerLetter):
                bot.send_message(message.chat.id, "Parabéns 🎉🎉!\nVocê ganhou da Velhinha, vamos /jogar novamente ou você pode voltar ao /menu")
                gameIsPlaying = False
            else:
                if jogo_velha.isBoardFull(theBoard):
                    bot.send_message(message.chat.id, "Ninguém ganhou essa!\nVamos /jogar denovo")
                    gameIsPlaying = False
                else:
                    isPlayer = False
            if gameIsPlaying:
                computer_move(message)
    else:
        bot.send_message(message.chat.id, "Inicie uma nova partida, em /jogar\nOu volte ao /menu")


def computer_move(message):
    global theBoard
    global playerLetter, computerLetter
    global isPlayer
    global gameIsPlaying

    bot.send_message(message.chat.id, "Minha vez")
    time.sleep(2)
    move = jogo_velha.getComputerMove(theBoard, computerLetter)
    jogo_velha.makeMove(theBoard, computerLetter, move)
    desenha(message)
    if jogo_velha.isWinner(theBoard, computerLetter):
        bot.send_message(message.chat.id, "Eu ganhei 👵🏽\nTente novamente, vamos /jogar ou volte ao /menu")
        gameIsPlaying = False
    else:
        if jogo_velha.isBoardFull(theBoard):
            bot.send_message(message.chat.id, "Ninguém ganhou essa!\nVamos /jogar novamente")
            gameIsPlaying = False
        else:
            isPlayer = True
            bot.send_message(message.chat.id, "Sua vez, pode escolher uma posição")


@bot.message_handler(commands=['eu', 'vc'])
def init_game(message):
    global theBoard
    global playerLetter, computerLetter
    global isPlayer
    global gameIsPlaying

    playerLetter, computerLetter = ['X', 'O']

    if message.text == '/eu':
        isPlayer = True
    else:
        isPlayer = False

    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('7', '8', '9')
    start_markup.row('4', '5', '6')
    start_markup.row('1', '2', '3')
    bot.send_message(message.chat.id, 'Vamos começar!!!', reply_markup=start_markup)

    desenha(message)

    gameIsPlaying = True
    if not isPlayer:
        computer_move(message)
    else:
        bot.send_message(message.chat.id, 'Pode iniciar')


bot.infinity_polling()