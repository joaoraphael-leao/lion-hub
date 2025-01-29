users = []
postsList = []

class Post:
    def __init__(self, title, content, author):
        self._title = title
        self._content = content
        self.author = author
        self.id = len(postsList) + 1
        self._image = None

    def setName(self, title):
        self._title = title

    def setContent(self, content):
        self._content = content

    def setImage(self, image_url):
        self._image = image_url

    def __str__(self):
        return f'{self._title}: {self._content}\nImagem: {self._image if self._image else "Sem imagem"}'

class User:
    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = password
        self._id = len(users) + 1
        self.posts = []

    def __str__(self):
        return f'{self._name} ({self._email})'

    def _generalEdit(self):
        option = input("""Opções:
        1) Editar Nome
        2) Editar Email
        3) Editar Senha
        """)

        if option == '1':
            self._name = input("Digite o novo nome: ")
            print("Nome alterado com sucesso!")
        elif option == '2':
            self._email = input("Digite o novo email: ")
            print("Email alterado com sucesso!")
        elif option == '3':
            self._password = input("Digite a nova senha: ")
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
        print(f"Post criado com sucesso: {post._title}")

    def deletePost(self):
        postId = input("Digite o ID do post a ser excluído: ")
        for post in postsList:
            if post.id == int(postId) and post in self.posts:
                postsList.remove(post)
                self.posts.remove(post)
                print("Post removido com sucesso!")
                return
        print("Você não tem permissão para deletar este post")

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

def add_user():
    name = input("Diga seu nome: ")
    email = input("Diga seu email: ")
    password = createPassword()
    user = User(name, email, password)  
    users.append(user)  
    print(f"Usuário {name} criado com sucesso!")

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
            add_user()
        elif opcao == '2':
            seeAllPosts()
        elif opcao == '3':
            userEmail = input("Digite seu email: ")
            myUser = None
            for user in users:
                if user._email == userEmail:
                    passwordAttempt = input("Digite sua senha: ")
                    if passwordAttempt == user._password:
                        myUser = user
                        break

            if not myUser:
                print("Email ou senha incorretos!")
                continue

            userOption = input("""
            Opções de Usuário:
            1) Postar Algo 
            2) Deletar Post
            3) Editar dados da conta
            4) Deletar Conta

            Escolha uma opção: """)

            if userOption == '1':
                myUser._createPost()
            elif userOption == '2':
                myUser.deletePost()
            elif userOption == '3':
                myUser._generalEdit()
            elif userOption == '4':
                myUser._removeAccount()
            else:
                print("Opção inválida!")
        elif opcao == '4':
            print("Até mais!")
            break
        else:
            print("Opção inválida!")

startApp()
