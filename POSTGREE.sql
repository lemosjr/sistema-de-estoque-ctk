-- Tabela para armazenar os usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

-- Tabela para armazenar os itens (bebidas)
CREATE TABLE itens (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    alcoolico BOOLEAN NOT NULL,
    marca VARCHAR(100),
    quantidade INTEGER NOT NULL,
    valor NUMERIC(10, 2) NOT NULL -- Ótimo para valores monetários
);

SELECT * FROM USUARIOS