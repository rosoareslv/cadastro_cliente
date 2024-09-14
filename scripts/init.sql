create database cadastro_cliente;

\c cadastro_cliente

create table clientes(
    id serial not null,
    nome varchar(50) not null,
    cpf varchar(11) not null,
    dataAniversario date
);