# MailChimp as a microservice

## Usage

### Add subscriber to a list

```coffee
# Storyscript

mailchimp add_subscriber list_name: 'Your_list_name' user_email: 'xxxx@gmail.com' first_name: 'John' last_name: 'Doe' status: 'subscribed/unsubscribed' address: 'user_address' phone: '+1xxxx' API_KEY: 'Mailchimp API key' USERNAME: 'Mailchimp Username'

```

### Delete subscriber from a list

```

omg exec delete -a list_name=<list_name> -a user_email=<user_email> -e API_KEY=<API_KEY> -e USERNAME= <username>

```

### Add Tags to a subcriber

```

omg exec add_tag -a list_name=<list_name> -a user_email=<user_email> -a tag= <tag_name> -e API_KEY=<API_KEY> -e USERNAME= <username>

```

### Update a subcriber

```

omg exec update_subscriber -a list_name=<list_name< -a user_email= <user_email> -a last_name= <last_name> -a phone=<phone_number> -a new_email=<new_email> -e API_KEY= <API_KEY> -e USERNAME= <username>

```
