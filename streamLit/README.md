# Description

Streamlit cheat sheet

[cheat-sheet](https://cheat-sheet.streamlit.app/)

[cheat-sheet](https://docs.streamlit.io/develop/quick-reference/cheat-sheet)

# Running

```bash
streamlit run simple_webapp/app.py # This will use the default port or the one specified in the .env file.
streamlit run simple_webapp/app.py --server.port 8080 # This will serve on the specified port.
```

With config.toml file :

```bash
mkdir -p ~/.streamlit
cp config.toml ~/.streamlit/
streamlit run simple_webapp/app.py # This will serve on the port specified in config.toml.
```

# Deployment

Go to [streamlit.io](streamlit.io)
