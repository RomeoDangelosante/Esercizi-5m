import requests
import json



def show_comments_posts(user_id):
    try:
        url = f"https://jsonplaceholder.typicode.com/user/{user_id}/posts"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        posts_utente: list[dict] = response.json()
        print(type(posts_utente))
        print(json.dumps(posts_utente, indent=4))
        for post in posts_utente:
            print(f"Post ID: {post['id']}, Title: {post['title']}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

def get_post_comments(post_id):
    try:
        url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        comments_post: list[dict] = response.json()
        print(type(comments_post))
        print(json.dumps(comments_post, indent=4))
        for comment in comments_post:
            print(f"Comment ID: {comment['id']}, Name: {comment['name']}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

def add_post(user_id, post_id, name, email, body):
    nuovo_post = {
        "userId": user_id,
        "postid": post_id,
        "name": name,
        "email": email,
        "body": body
    }
    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/comments", json=nuovo_post
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Errore nella creazione del commento: {err}")
        return None

def main():
    user_id = 1

    # 1. Recupera tutti i post pubblicati dall'utente con ID = 1
    posts = show_comments_posts(user_id)
    if posts is None:
        return

    print("--- Post dell'utente 1 ---")
    for post in posts:
        print(f"ID Post: {post['id']}, Titolo: {post['title']}")

    if not posts:
        print("Nessun post trovato.")
        return

    # Ottieni l'ID del primo post
    first_post_id = posts[0]["id"]

    # 2. Recupera i commenti per il primo post
    comments = get_post_comments(first_post_id)
    if comments is None:
        return

    print("\n--- Commenti per il primo post ---")
    for comment in comments:
        print(f"- {comment['name']}: {comment['body']}")

    # 3. Crea un nuovo commento per il primo post
    new_comment = add_post(
        post_id=first_post_id,
        name="Nuovo Commentatore",
        email="nuovo@example.com",
        body="Questo è un commento aggiunto tramite API!",
    )
    if new_comment is None:
        return

    print("\n--- Nuovo Commento Creato ---")
    print(new_comment)


if __name__ == "__main__":
    main()