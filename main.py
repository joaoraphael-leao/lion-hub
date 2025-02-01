users = []
postsList = []

## coisas a implementar, lista de pessoas que curtiram
class Post:
    def __init__(self, title, content, author):
        self._title = title
        self._content = content
        self._author = author
        self._likes = 0
        self._coments = []
        self.id = len(postsList) + 1
        self._image = None


    def get_author(self):
        return self._author

    def getTitle(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def getContent(self):
        return self._content

    def setContent(self, content):
        self._content = content

    def getImage(self):
        return self._image

    def setImage(self, image_url):
        self._image = image_url

    def _update_likes(self):
        self._likes += 1
    def getLikes(self):
        return self._likes

    def __str__(self):
        return f"{self.get_author().getName()} Postou:\n{self._title}: {self._content}\nLikes: {self.getLikes()}"



class User:
    def __init__(self, name, email, password, privacity):
        self._name = name
        self._email = email
        self._password = password
        self._id = len(users) + 1
        self.posts = []
        self._notifications = []
        self._followingList = []
        self._followersList = []
        self._privacity = privacity

    def add_notification(self, notification):
        self._notifications.append(notification)
    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getPassword(self):
        return self._password

    def setPassword(self, password):
        self._password = password

    def getId(self):
        return self._id

    def getFollowingList(self):
        return self._followingList

    def __str__(self):
        return f"""   {self._name}\n   {self._email}\n"""

    def _generalEdit(self):
        option = input("""Opções:
        1) Editar Nome
        2) Editar Email
        3) Editar Senha
        """)

        if option == '1':
            self.setName(input("Digite o novo nome: "))
            print("Nome alterado com sucesso!")
        elif option == '2':
            self.setEmail(input("Digite o novo email: "))
            print("Email alterado com sucesso!")
        elif option == '3':
            self.setPassword(input("Digite a nova senha: "))
            print("Senha alterada com sucesso!")
        else:
            print("Opção inválida!")
            self._generalEdit()

    def _removeAccount(self):
        users.remove(self)
        print("Conta removida com sucesso!")

    def _createPost(self):
        title = input("Qual o título do seu post? ")
        content = input("O que você quer dizer? ")
        post = Post(title, content, self)
        imageQuestion = input("Você quer adicionar uma imagem? (y/n) ")
        if imageQuestion.lower() == 'y':
            image = input("Digite o URL da imagem: ")
            post.setImage(image)
        postsList.append(post)
        self.posts.append(post)
        print(f"Post criado com sucesso: {post.getTitle()}")

    def deletePost(self):
        postId = input("Digite o ID do post a ser excluído: ")
        for post in postsList:
            if post.id == int(postId) and post in self.posts:
                postsList.remove(post)
                self.posts.remove(post)
                print("Post removido com sucesso!")
                return
        print("Você não tem permissão para deletar este post")

    def follow_someone(self):
        print("Escolha alguém para seguir")
        showUsers(myUser=self)
        followed_profile_name = input()
        for user in users:
            if followed_profile_name == user.getName():
                self._followingList.append(user.getName())
                user._notifications.append({
                    "user": self.getName(),
                   "message" : f"{self.getName()} começou a te seguir",
                    "is_follow_notification": True,
                })

    def show_notifications(self):
        for notification in self._notifications:
            if(notification["is_follow_notification"]):
                follow_back = input(notification["message"] + ", deseja seguí-lo de volta ? (y/n)")
                if follow_back == "y":
                    self._followingList.append(notification["user"])
                    notification["user"]._notifications.append({
                        "message": f"{self.getName()} te seguiu de volta!",
                    })
            else:
                print(notification["message"])

    def like_post(self, post_to_like):
        post_to_like._update_likes
        post_author = post_to_like.getAuthor()
        notification = {
            "message": f"{self.getName()} curtiu sua foto"
        }
        post_author.add_notification(notification)


def seeAllPosts():
    if not postsList:
        print("Nenhum post disponível.")
    for post in postsList:
        print(post)


def createPassword():
    while True:
        password = input("Digite sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
        if password == confirmPassword:
            return password
        print("Senhas não conferem! Tente novamente.")


def add_new_user():
    name = input("Diga seu nome: ")
    email = input("Diga seu email: ")
    password = createPassword()

    privacity = False
    privacity_option = input("Seu perfil será privado? (y/n)")
    if privacity_option == 'y':
        privacity = True

    user = User(name, email, password, privacity= privacity)
    users.append(user)
    print(f"Usuário {name} criado com sucesso!")


def showUsers(myUser):
    for i, user in enumerate(users):
        if user == myUser:
            continue
        print(f"""Usuario {i + 1}: 
    {user.getName()}""")


def startApp():
    while True:
        opcao = input("""
        Bem-vindo à rede social!

        1) Criar conta
        2) Ver posts
        3) Opções de Usuário
        4) Sair

        Escolha uma opção: """)

        if opcao == '1':
            add_new_user()
        elif opcao == '2':
            seeAllPosts()
        elif opcao == '3':
            userEmail = input("Digite seu email: ")
            myUser = next((user for user in users if user.getEmail() == userEmail), None)

            if not myUser:
                print("Email ou senha incorretos!")
                continue

            userOption = input("""
            Opções de Usuário:
            1) Postar Algo 
            2) Deletar Post
            3) Editar dados da conta
            4) Deletar Conta
            5) Ver usuários
            6) Exibir notificações
            7) Seguir novas pessoas
            Escolha uma opção: """)

            if userOption == '1':
                myUser._createPost()
            elif userOption == '2':
                myUser.deletePost()
            elif userOption == '3':
                myUser._generalEdit()
            elif userOption == '4':
                myUser._removeAccount()
            elif userOption == '5':
                showUsers()
            elif userOption == '6':
               myUser.show_notifications()
            elif userOption == '7':
                myUser.follow_someone()
            else:
                print("Opção inválida!")
        elif opcao == '4':
            print("Até mais!")
            break
        else:
            print("Opção inválida!")


startApp()
