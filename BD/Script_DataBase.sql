-- Criação do Banco de dados 

create database LocaCar;
use LocaCar;

-- Criação da tabela "Cliente"
CREATE TABLE Cliente (
    ID_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255),
    Telefone VARCHAR(12)
);

-- Criação da tabela "Tipo_Carro"
CREATE TABLE Tipo_Carro (
    ID_Tipo INT AUTO_INCREMENT  PRIMARY KEY,
    Nome_tipo VARCHAR(255),
    Valor_dias FLOAT,
    Valor_semanal FLOAT,
    valor_taxa_atraso FLOAT
);

-- Criação da tabela "Carro"
CREATE TABLE Carro (
    ID_Carro INT AUTO_INCREMENT PRIMARY KEY,
    ID_Tipo INT,
    Modelo VARCHAR(255),
    Marca VARCHAR(255),
    Ano VARCHAR(4),
    FOREIGN KEY (ID_Tipo) REFERENCES Tipo_Carro (ID_Tipo)
);

-- Criação da tabela "Aluguel"
CREATE TABLE Aluguel (
    ID_Aluguel INT AUTO_INCREMENT PRIMARY KEY,
    ID_Carro int,
    ID_Cliente INT,
    Status_Tipo VARCHAR(20),
    Data_inicio DATE,
    Numero_dias INT,
    Data_retorno DATE,
    Valor_Total float,
    Valor_pago Float,
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente (ID_Cliente),
    FOREIGN KEY (ID_Carro) REFERENCES Carro (ID_Carro)
);


-- Criação de Trigger para impedir que exclusão de carros associados a aluguies"

DELIMITER //
CREATE TRIGGER impede_exclusao_carro
BEFORE DELETE ON Carro
FOR EACH ROW
BEGIN
    DECLARE aluguel_count INT;

    -- Verifica se existem aluguéis associados a este carro
    SELECT COUNT(*) INTO aluguel_count
    FROM Aluguel
    WHERE ID_Carro = OLD.ID_Carro;

    -- Se houver aluguéis associados, cancela a exclusão
    IF aluguel_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Este carro não pode ser excluído, pois está associado a aluguéis.';
    END IF;
END;
//
DELIMITER ;
