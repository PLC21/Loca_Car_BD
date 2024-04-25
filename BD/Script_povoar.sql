use locacar;
    
INSERT INTO Tipo_Carro (Nome_tipo, Valor_dias, Valor_semanal, valor_taxa_atraso)
VALUES
    ('COMPACTO', 200.0, 1200.0, 100),
    ('MÉDIO', 220.0, 1300.0, 200),
    ('GRANDE', 250.0, 1500.0, 300),
    ('SUV', 350.0, 2200.0, 400),
    ('CAMINHÃO', 2500.0, 350.0, 500);

-- Inserindo carros COMPACTO
INSERT INTO Carro (ID_Tipo, Modelo, Marca, Ano)
VALUES 
	(1, 'Fiat Uno', 'Fiat', '2023'),
	(1, 'Volkswagen Gol', 'Volkswagen', '2023'),
	(1, 'Renault Kwid', 'Renault', '2023'),
	(1, 'Chevrolet Onix', 'Chevrolet', '2023'),
	(1, 'Hyundai HB20', 'Hyundai', '2023');

-- Inserindo carros MÉDIO
INSERT INTO Carro (ID_Tipo, Modelo, Marca, Ano)
VALUES 
	(2, 'Toyota Corolla', 'Toyota', '2023'),
	(2, 'Honda Civic', 'Honda', '2023'),
	(2, 'Nissan Sentra', 'Nissan', '2023'),
	(2, 'Mazda 3', 'Mazda', '2023'),
	(2, 'Kia Cerato', 'Kia', '2023');

-- Inserindo carros GRANDE
INSERT INTO Carro (ID_Tipo, Modelo, Marca, Ano)
VALUES 
	(3, 'Ford Fusion', 'Ford', '2023'),
	(3, 'Chevrolet Impala', 'Chevrolet', '2023'),
	(3, 'Buick LaCrosse', 'Buick', '2023'),
	(3, 'Dodge Charger', 'Dodge', '2023'),
	(3, 'Chrysler 300', 'Chrysler', '2023');

-- Inserindo carros SUV
INSERT INTO Carro (ID_Tipo, Modelo, Marca, Ano)
VALUES 
	(4, 'Jeep Grand Cherokee', 'Jeep', '2023'),
	(4, 'Toyota RAV4', 'Toyota', '2023'),
	(4, 'Honda CR-V', 'Honda', '2023'),
	(4, 'Ford Escape', 'Ford', '2023'),
	(4, 'Subaru Outback', 'Subaru', '2023');

-- Inserindo carros CAMINHÃO
INSERT INTO Carro (ID_Tipo, Modelo, Marca, Ano)
VALUES 
	(5, 'Ford F-150', 'Ford', '2023'),
	(5, 'Chevrolet Silverado', 'Chevrolet', '2023'),
	(5, 'Ram 1500', 'Ram', '2023'),
	(5, 'GMC Sierra', 'GMC', '2023'),
	(5, 'Toyota Tundra', 'Toyota', '2023');


-- Inserindo clientes com nomes de músicos e rappers famosos
INSERT INTO Cliente (Nome, Telefone)
VALUES
    ('Eminem', '66-5555-5555'),
    ('Beyoncé', '66-6666-6666'),
    ('Jay-Z', '66-7777-7777'),
    ('Ariana Grande', '66-8888-8888'),
    ('Drake', '66-9999-9999'),
    ('Kanye West', '66-0000-0000'),
    ('Taylor Swift', '66-1111-1111'),
    ('Rihanna', '66-2222-2222'),
    ('Lady Gaga', '66-3333-3333'),
    ('Kendrick Lamar', '66-4444-4444'),
    ('Travis Scott', '66-5555-5555'),
    ('Cardi B', '66-6666-6666'),
    ('Nicki Minaj', '66-7777-7777'),
    ('The Weeknd', '66-8888-8888'),
    ('Post Malone', '66-9999-9999'),
    ('Adele', '66-0000-0000'),
    ('Justin Bieber', '66-1111-1111'),
    ('Billie Eilish', '66-2222-2222'),
    ('Ed Sheeran', '66-3333-3333'),
    ('Shawn Mendes', '66-4444-4444'),
    ('Alicia Keys', '66-5555-5555'),
    ('Snoop Dogg', '66-6666-6666');
