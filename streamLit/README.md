# Description

Streamlit cheat sheet

[cheat-sheet](https://cheat-sheet.streamlit.app/)
[cheat-sheet](https://docs.streamlit.io/develop/quick-reference/cheat-sheet)

# Running

```bash
streamlit run simple_webapp/app.py # This will provide default port or .env file
streamlit run simple_webapp/app.py --server.port 8080 # This will serve in the specificed port
```

With config.toml file :

```bash
mkdir -p ~/.streamlit
cp config.toml ~/.streamlit/
```