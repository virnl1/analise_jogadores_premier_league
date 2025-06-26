import pandas as pd

# Exemplo de criação de um DataFrame (substitua pelo seu próprio DataFrame)
df = pd.DataFrame({
    "Player Name": ["Alice", "Bob"],
    "Score": [10, 20]
})

# Renomear colunas (opcional)
df.rename(columns={
    "Player Name": "Player",
    # adicione mais renomeações aqui se quiser simplificar os nomes
}, inplace=True)