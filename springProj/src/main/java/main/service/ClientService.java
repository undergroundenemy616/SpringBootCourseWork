package main.service;

import main.entity.Clients;

import java.util.List;

public interface ClientService {
    List<Clients> listClients();
    Clients findClient(Integer id);
    Clients addClient(Clients journal);
}
