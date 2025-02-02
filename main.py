users = []
posts_list = []
events = []
groups = []

## coisas a implementar, lista de pessoas que curtiram
class Event:
    def __init__(self, event_name, event_date, event_location, event_description):
        self._event_name = event_name
        self._event_date = event_date
        self._event_location = event_location
        self._event_description = event_description
        self._participants = []
        self._id = len(events) + 1

    def __str__(self):
        return f"Evento: {self._event_name}\n    Data: {self._event_date}\n    Local: {self._event_location}\n    Descrição: {self._event_description}\n"

    def get_event_name(self):
        return self._event_name

    def get_event_date(self):
        return self._event_date
    def get_participants(self):
        return self._participants
    def invite_people(self, participant):
        non_participants = list(filter (lambda user: user not in self.get_participants(), users))
        for user in non_participants:
            print(f"{user.get_id()} {user.getName()}")
    def get_id(self):
        return self._id

def create_event(current_user):
    print("\n--- Criando um novo evento ---")
    name = input("Digite o nome do evento: ")
    date = input("Digite a data do evento (ex: 2025-02-01): ")
    location = input("Digite o local do evento: ")
    description = input("Digite a descrição do evento: ")
    new_event = Event(name, date, location, description)
    events.append(new_event)
    # Adiciona automaticamente o criador como participante
    new_event._participants.append(current_user)
    print("Evento criado com sucesso!")
    return new_event

def list_events():
    if not events:
        print("Nenhum evento disponível.")
        return
    print("\n--- Eventos Disponíveis ---")
    for event in events:
        print(f"ID: {event.get_id()} - {event.get_event_name()} (Data: {event.get_event_date()})")

def invite_to_event(current_user):
    if not events:
        print("Nenhum evento disponível para convidar pessoas.")
        return
    list_events()
    try:
        event_id = int(input("Digite o ID do evento para convidar pessoas: "))
    except ValueError:
        print("ID inválido.")
        return
    event = next((e for e in events if e.get_id() == event_id), None)
    if event is None:
        print("Evento não encontrado.")
        return
    # Lista os usuários que ainda não fazem parte do evento
    available_users = [user for user in users if user not in event.get_participants()]
    if not available_users:
        print("Nenhum usuário disponível para convidar.")
        return
    print("\n--- Usuários Disponíveis para Convidar ---")
    for user in available_users:
        print(f"{user.get_id()} - {user.getName()}")
    invite_ids = input("Digite os IDs dos usuários para convidar (separados por vírgula): ")
    invite_ids_list = invite_ids.split(',')
    for id_str in invite_ids_list:
        try:
            uid = int(id_str.strip())
        except ValueError:
            continue
        invited_user = next((u for u in available_users if u.get_id() == uid), None)
        if invited_user:
            event._participants.append(invited_user)
            invited_user.add_notification({
                "user": current_user,
                "message": f"{current_user.getName()} te convidou para o evento '{event._event_name}'.",
                "is_event_invite": True,
                "event_id": event.get_id()
            })
            print(f"Usuário {invited_user.getName()} convidado para o evento.")

def show_event_details():
    if not events:
        print("Nenhum evento disponível.")
        return
    try:
        event_id = int(input("Digite o ID do evento para ver detalhes: "))
    except ValueError:
        print("ID inválido.")
        return
    event = next((e for e in events if e.get_id() == event_id), None)
    if event is None:
        print("Evento não encontrado.")
        return
    print("\n--- Detalhes do Evento ---")
    print(event)
    if event.get_participants():
        print("Participantes:")
        for participant in event.get_participants():
            print(f"- {participant.getName()}")
    else:
        print("Nenhum participante inscrito no evento.")

class Post:
    def __init__(self, title, content, author):
        self._title = title
        self._content = content
        self._author = author
        self._likes = 0
        self._comments = []
        self._id = len(posts_list) + 1
        self._image = None
        self._video = None

    def get_comments(self):
        return self._comments

    def get_author(self):
        return self._author

    def get_title(self):
        return self._title
    def edit_title(self, title, user):
        if user == self.get_author():
            self._title = title

    def get_content(self):
        return self._content

    def edit_content(self, content, user):
        if user == self.get_author():
            self._content = content

    def get_image(self):
        return self._image

    def set_image(self, image_url):
        self._image = image_url

    def _update_likes(self):
        self._likes += 1
    def getLikes(self):
        return self._likes
    def get_id(self):
        return self._id
    def __str__(self):
        return f"ID:{self.get_id()} Autor:{self.get_author().getName()}:\n    {self._title}: {self._content}\nLikes: {self.getLikes()}"

class User:
    def __init__(self, name, email, password, privacity):
        self._name = name
        self._email = email
        self._password = password
        self._id = len(users) + 1
        self._notifications = []
        self._followingList = []
        self._followersList = []
        self._privacity = privacity
        self._active = True

    def __str__(self):
        return f"""   {self._name}\n   {self._email}\n"""

    def getName(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_id(self):
        return self._id

    ## nao remove da lista senao tenho bugs com o id.
    def _delete_account(self):
        for post in posts_list[:]:
            if post.get_author() == self:
                posts_list.remove(post)
        self._name = ""
        self._email = ""
        self._password = ""
        self._notifications = []
        self._followingList = []
        self._followersList = []
        self._active = False  # Marca como inativo
        print("Conta desativada com sucesso!")

    def _general_edit(self):
        while True:
            option = input("""Opções:
            1) Editar Nome
            2) Editar Email
            3) Editar Senha
            Escolha uma opção: """)

            if option == '1':
                self.set_name(input("Digite o novo nome: "))
                print("Nome alterado com sucesso!")
                break
            elif option == '2':
                self.set_email(input("Digite o novo email: "))
                print("Email alterado com sucesso!")
                break
            elif option == '3':
                self.set_password(input("Digite a nova senha: "))
                print("Senha alterada com sucesso!")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def _createPost(self):
        title = input("Qual o título do seu post? ")
        content = input("O que você quer dizer? ")
        post = Post(title, content, self)
        image_question = input("Você quer adicionar uma imagem? (y/n) ")
        if image_question.lower() == 'y':
            image = input("Digite o URL da imagem: ")
            post.set_image(image)

        video_question = input("Você quer adicionar um video ? (y/n) ")
        if video_question.lower() == 'y':
            video = input("Digite o URL do vídeo: ")
            post._video = video

        posts_list.append(post)
        print(f"Post criado com sucesso: {post.get_title()}")

    def delete_post(self):
        my_posts = [post for post in posts_list if post.get_author() == self]

        if not my_posts:
            print("Nenhum post encontrado para deletar.")
            return
        for post in my_posts:
            print(post)

        postId = input("Digite o ID do post a ser excluído: ")

        for post in my_posts:
            if post.get_id() == int(postId):
                posts_list.remove(post)
                print("Post removido com sucesso!")
                return
        print("Você não tem permissão para deletar este post ou ele não existe")

    def getFollowingList(self):
        return self._followingList

    def getFollowersList(self):
        print(f"People who follows {self.getName()}")
        for person in self._followersList:
            print(person.getName())

    def follow_someone(self):
        print("Escolha alguém para seguir")
        show_users(my_user=self)
        followed_profile_name = input("Digite o nome do usuário a seguir: ")
        for user in users:
            if followed_profile_name == user.getName():
                # Se for privado, envia solcitação, caso contrário, já segue.
                if user._privacity:
                    user.add_notification({
                        "user": self,
                        "message": f"{self.getName()} solicitou para te seguir",
                        "is_follow_notification": True,
                        "follow_request": True
                    })
                    print(f"Solicitação para seguir {user.getName()} enviada")
                else:
                    self._followingList.append(user)
                    user.add_notification({
                        "user": self,
                        "message": f"{self.getName()} começou a te seguir",
                        "is_follow_notification": True
                    })
                    print(f"Você começou a seguir {user.getName()}")
                return
        print("Não encontramos esse usuário! Verifique se o nome foi digitado corretamente.")


    def add_notification(self, notification):
        self._notifications.append(notification)


    def _follow_notification_interaction(self, notification):
        ## Se for solicitação para seguir, segue um fluxo, senao, segue outro fluxo
        if notification.get(["follow_request"], False):
            print(notification["message"])
            decision = input(f"Aceita a solicitação para te seguir de {notification['user'].getName()}? (y/n): ")
            if decision.lower() == 'y':
                self._followersList.append(notification["user"])
                notification["user"].add_notification({
                    "user": self,
                    "message": f"{self.getName()} aceitou sua solicitação de seguir.",
                    "is_follow_notification": True
                })
                print(f"Você agora permite que {notification['user'].getName()} te siga.")
            else:
                notification["user"].add_notification({
                    "user": self,
                    "message": f"{self.getName()} rejeitou sua solicitação de seguir.",
                    "is_follow_notification": True
                })
                print("Você rejeitou a solicitação para seguir.")
        else:
            print(notification["message"])
            follow_back = input("Deseja segui-lo de volta? (y/n): ")
            if follow_back.lower() == "y":
                self._followingList.append(notification["user"])
                notification["user"].add_notification({
                    "user": self,
                    "message": f"{self.getName()} te seguiu de volta!",
                    "is_follow_notification": True
                })
    def show_all_notifications(self):
        for notification in self._notifications:
            if notification.get(["is_follow_notification"], False):
                self._follow_notification_interaction(notification)
            else:
                print(notification["message"])

    def _see_likes(self):
        likes = list(filter(lambda notification: notification.get("is_like", False), self._notifications))
        for like in likes:
            print(f"{like['user'].getName()} curtiu sua foto")

    def _see_comments(self):
        comments = list(filter(lambda notification: notification.get("is_comment", False), self._notifications))
        for comment in comments:
            print(f"{comment['user'].getName()} comentou seu post: {comment['comment']}")

    def _see_follow_notifications(self):
        follow_notifications = list(filter(lambda notification: notification["is_follow_notification"], self._notifications))
        for notification in follow_notifications:
            self._follow_notification_interaction(notification)

    def _show_private_message_notifications(self):
        messages = list(filter(lambda notification: notification.get(["is_message"], False), self._notifications))
        for message in messages:
            print(f"{message['user'].getName()} te enviou uma mensagem: {message['message']}")
class Group:
    def __init__(self, name, description, founder):
        self._name = name
        self._founder = founder
        self._description = description or ""
        self._members = []
        self._posts = []
        self._messages = []
    def __str__(self):
        return f"{self._name}\n{len(self._members)} Participantes"

    def show_group_members(self):
        for i, member in enumerate(self._members):
            print(f"Participant {i + 1}: {member.getName()}")
    def show_group_description(self):
        print(f"Descrição: {self._description}")

    def _add_member(self, member):
        if member in self._members:
            print(f"{member.getName()} já faz parte do grupo {self._name}")
        else:
            self._members.append(member)
            print(f"{member.getName()} adicionado ao grupo {self._name}")

    def _remove_member(self, member):
        self._members.remove(member)
        print(f"{member.getName()} removido do grupo {self._name}")

def create_group(current_user):
    print("\n--- Criando um novo grupo ---")
    name = input("Digite o nome do grupo: ")
    description = input("Digite a descrição do grupo: ")
    # Cria o grupo e adiciona o fundador como membro
    new_group = Group(name, description, current_user)
    new_group._members.append(current_user)
    groups.append(new_group)
    print(f"Grupo '{name}' criado com sucesso!")
    return new_group

def list_groups():
    if not groups:
        print("Nenhum grupo disponível.")
        return
    print("\n--- Grupos Disponíveis ---")
    for i, group in enumerate(groups, start=1):
        print(f"{i}) {group._name} - {len(group._members)} participantes")

def manage_group(current_user):
    user_groups = [group for group in groups if group._founder == current_user or current_user in group._members]
    if not user_groups:
        print("Você não participa de nenhum grupo.")
        return
    print("\n--- Seus Grupos ---")
    for i, group in enumerate(user_groups, start=1):
        print(f"{i}) {group._name}")
    try:
        choice = int(input("Digite o número do grupo que deseja gerenciar: "))
        selected_group = user_groups[choice - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return
    while True:
        print(f"\n--- Gerenciando o grupo '{selected_group._name}' ---")
        print("1) Ver membros")
        print("2) Adicionar membro")
        print("3) Remover membro")
        print("4) Voltar")
        option = input("Escolha uma opção: ")
        if option == '1':
            selected_group.show_group_members()
        elif option == '2':
            show_users(current_user)
            try:
                uid = int(input("Digite o ID do usuário que deseja adicionar: "))
            except ValueError:
                print("ID inválido.")
                continue
            user_to_add = next((user for user in users if user.get_id() == uid), None)
            if user_to_add:
                selected_group._add_member(user_to_add)
            else:
                print("Usuário não encontrado.")
        elif option == '3':
            selected_group.show_group_members()
            try:
                uid = int(input("Digite o ID do usuário que deseja remover: "))
            except ValueError:
                print("ID inválido.")
                continue
            user_to_remove = next((user for user in selected_group._members if user.get_id() == uid), None)
            if user_to_remove:
                if user_to_remove == selected_group._founder:
                    print("Não é possível remover o fundador do grupo.")
                else:
                    selected_group._remove_member(user_to_remove)
            else:
                print("Usuário não encontrado no grupo.")
        elif option == '4':
            break
        else:
            print("Opção inválida!")

def message_someone(current_user):
    print("Escolha alguém para enviar mensagem")
    show_users(my_user=current_user)
    target_username = input("Digite o nome do usuário: ")
    target_user = next((u for u in users if u.getName() == target_username), None)
    if not target_user:
        print("Usuário não encontrado")
        return
    message = input("Digite sua mensagem: ")
    target_user.add_notification({
        "user": current_user,
        "message": message,
        "is_message": True
    })
    print("Mensagem enviada com sucesso!")

def like_post(seeing_user, post_to_like):
    post_to_like._update_likes()
    post_author = post_to_like.get_author()
    notification = {
        "user": seeing_user,
        "message": f"{seeing_user.getName()} curtiu sua foto",
        "is_like": True
    }
    post_author.add_notification(notification)

def comment_post(seeing_user, post_to_comment):
    comment = input("Digite seu comentário: ")
    post_to_comment._comments.append({
        "user": seeing_user.getName(),
        "comment": comment
    })
    post_author = post_to_comment.get_author()
    notification = {
        "user": seeing_user,
        "message": f"{seeing_user.getName()} comentou seu post: {comment}",
        "is_comment": True,
        "comment": comment
    }
    post_author.add_notification(notification)
def search_posts(seeing_user):
    search = input("Digite o que você quer pesquisar: ")
    posts_to_see = list(filter(lambda post: (search.lower() in post.get_title().lower() or search.lower() in post.get_content().lower()) and (not post.get_author()._privacity or post.get_author() in seeing_user.getFollowingList()), posts_list))

    for post in posts_to_see:
        print(post)
        for comment in post.get_comments():
            print(comment["user"] + " " + comment["comment"])

def edit_post(current_user):
    my_posts = [post for post in posts_list if post.get_author() == current_user]
    if not my_posts:
        print("Você não possui posts para editar.")
        return
    print("\n--- Seus Posts ---")
    for post in my_posts:
        print(post)
    try:
        post_id = int(input("Digite o ID do post que deseja editar: "))
    except ValueError:
        print("ID inválido.")
        return
    selected_post = next((post for post in my_posts if post.get_id() == post_id), None)
    if not selected_post:
        print("Post não encontrado.")
        return
    while True:
        print("\nOpções de Edição:")
        print("1) Editar Título")
        print("2) Editar Conteúdo")
        print("3) Voltar")
        op = input("Escolha uma opção: ")
        if op == '1':
            novo_titulo = input("Digite o novo título: ")
            selected_post.edit_title(novo_titulo, current_user)
            print("Título editado com sucesso!")
        elif op == '2':
            novo_conteudo = input("Digite o novo conteúdo: ")
            selected_post.edit_content(novo_conteudo, current_user)
            print("Conteúdo editado com sucesso!")
        elif op == '3':
            break
        else:
            print("Opção inválida!")

def see_user_posts(author):
    user_posts = [post for post in posts_list if post.get_author() == author]
    if not user_posts:
        print("Nenhum post encontrado para este usuário.")
        return
    print(f"\n--- Posts de {author.getName()} ---")
    for post in user_posts:
        print(post)
        print("")

def see_all_posts(seeing_user):
    if not posts_list:
        print("Nenhum post disponível.")
        return
    print("\n--- Todos os Posts ---")
    for post in posts_list:
        if post.get_author()._privacity and post.get_author() not in seeing_user.getFollowingList():
            continue
        print(post)
        for comment in post.get_comments():
            print(f"{comment['user']} : {comment['comment']}")
            print("")
    print("Fim dos posts")

    like_id_string = input("Digite o ID do post que deseja curtir: ")
    try:
        like_id = int(like_id_string)
    except ValueError:
        print("ID inválido.")
        return
    selected_post = next((post for post in posts_list if post.get_id() == like_id), None)
    if selected_post:
        like_post(seeing_user, selected_post)
    else:
        print("Post não encontrado.")

def createPassword():
    while True:
        password = input("Digite sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
        if password == confirmPassword:
            return password
        print("Senhas não conferem! Tente novamente.")


def add_new_user():
    username_exists = lambda username: any(user.getName() == username for user in users)
    email = input("Diga seu email: ")
    username = input("Diga seu nome: ")
    if username_exists(username=username):
        print("Esse nome não está disponível")
        return add_new_user()  # Chama novamente para tentar outro nome
    else:
        password = createPassword()
        privacity = False
        privacity_option = input("Seu perfil será privado? (y/n) ")
        if privacity_option.lower() == 'y':
            privacity = True
        user = User(username, email, password, privacity)
        users.append(user)
        print(f"Usuário {username} criado com sucesso!")
        return user


def show_users(my_user):
    for i, user in enumerate(users):
        if not user._active or user.getName() == "":
            continue
        if user == my_user:
            continue
        print(f"Usuário {i + 1}: \n    {user.getName()}")

def posts_menu(my_user):
    while True:
        print("Menu de Posts:")
        print("1) Criar Post")
        print("2) Editar Post")  # Nova opção de edição
        print("3) Deletar algum Post")
        print("4) Ver todos os posts")
        print("5) Pesquisar posts")
        print("6) Voltar")
        choice = input("Escolha uma das opções acima: ")
        if choice == '1':
            my_user._createPost()
            break
        elif choice == '2':
            edit_post(my_user)
            break
        elif choice == '3':
            my_user.delete_post()
            break
        elif choice == '4':
            see_all_posts(my_user)
            break
        elif choice == '5':
            search_posts(seeing_user=my_user)
            break
        elif choice == '6':
            break
        else:
            print("Opção inválida!")

def group_menu(current_user):
    while True:
        print("\nMenu de Grupos:")
        print("1) Criar Grupo")
        print("2) Listar Grupos")
        print("3) Gerenciar Meus Grupos")
        print("4) Voltar")
        op = input("Escolha uma opção: ")
        if op == '1':
            create_group(current_user)
            break
        elif op == '2':
            list_groups()
            break
        elif op == '3':
            manage_group(current_user)
            break
        elif op == '4':
            break
        else:
            print("Opção inválida!")

def account_menu(my_user):
    while True:
        print("Menu da Conta:")
        print("1) Editar dados da conta")
        print("2) Deletar Conta")
        print("3) Voltar")

        choice = input("Escolha uma das opções acima: ")

        if choice == '1':
            my_user._general_edit()
            break
        elif choice == '2':
            my_user._delete_account()
            break
        elif choice == '3':
            break
        else:
            print("Opção inválida!")

def notifications_menu(my_user):
    while True:
        print("Menu de Notificações:")
        print("1) Ver todas as notificações")
        print("2) Ver notificações de curtidas")
        print("3) Ver notificações de comentários")
        print("4) Ver notificações de seguidores")
        print("5) Voltar")

        choice = input("Escolha uma das opções acima: ")

        if choice == '1':
            my_user.show_all_notifications()
            break
        elif choice == '2':
            my_user._see_likes()
            break
        elif choice == '3':
            my_user._see_comments()
            break
        elif choice == '4':
            my_user._see_follow_notifications()
            break
        elif choice == '5':
            break
        else:
            print("Opção inválida!")
def social_menu(my_user):
    while True:
        print("Menu Social:")
        print("1) Seguir novas pessoas")
        print("2) Ver usuários")
        print("3) Enviar mensagens para alguém")
        print("4) Voltar")

        choice = input("Escolha uma das opções acima: ")

        if choice == '1':
            my_user.follow_someone()
            break
        elif choice == '2':
            show_users(my_user)
            break
        elif choice == '3':
            message_someone(my_user)
            break
        elif choice == '4':
            break
        else:
            print("Opção inválida!")


def events_menu(current_user):
    while True:
        print("\nMenu de Eventos:")
        print("1) Criar Evento")
        print("2) Convidar Pessoas para Evento")
        print("3) Listar Eventos")
        print("4) Ver detalhes do Evento")
        print("5) Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            create_event(current_user)
            break
        elif choice == '2':
            invite_to_event(current_user)
            break
        elif choice == '3':
            list_events()
            break
        elif choice == '4':
            show_event_details()
            break
        elif choice == '5':
            break
        else:
            print("Opção inválida!")

def user_options_menu(my_user):
    while True:
        if my_user._active == False:
            print("Sua conta foi desativada. Você será redirecionado para a tela de login.")
            break
        print("\nOpções de Usuário:")
        print("1) Menu de Posts")
        print("2) Menu da Conta")
        print("3) Menu de Notificações")
        print("4) Menu Social")
        print("5) Menu de Eventos")
        print("6) Menu de Grupos")  # Nova opção para grupos
        print("7) Sair")
        user_choice = input("Escolha uma das opções: ")
        if user_choice == '1':
            posts_menu(my_user)
        elif user_choice == '2':
            account_menu(my_user)
        elif user_choice == '3':
            notifications_menu(my_user)
        elif user_choice == '4':
            social_menu(my_user)
        elif user_choice == '5':
            events_menu(my_user)
        elif user_choice == '6':
            group_menu(my_user)
        elif user_choice == '7':
            break
        else:
            print("Opção inválida!")
def general_menu():
    option = ""
    while option != '3':
        option = input("""
        Bem-vindo à rede social!

        1) Criar conta
        2) Login
        3) Sair

        Escolha uma opção: """)

        if option == '1':
            my_user = add_new_user()
            user_options_menu(my_user=my_user)
        elif option == '2':
            userEmail = input("Digite seu email: ")
            userPassword = input("Digite sua senha: ")
            my_user = next(
                (user for user in users if user.get_email() == userEmail and user.get_password() == userPassword), None)
            if not my_user:
                print("Email ou senha incorretos!")
                continue
            user_options_menu(my_user=my_user)
        elif option != '3':
            print("Opção inválida!")



general_menu()
