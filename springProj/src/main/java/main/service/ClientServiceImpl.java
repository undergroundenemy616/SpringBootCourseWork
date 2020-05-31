package main.service;

import main.entity.Books;
import main.entity.Clients;
import main.exception.JournalNotFoundException;
import main.repository.ClientsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ClientServiceImpl implements ClientService{

    @Autowired
    private ClientsRepository clientsRepository;

    @Override
    public List<Clients> listClients() {
        return (List<Clients>) clientsRepository.findAll();
    }

    @Override
    public Clients findClient(Integer id) {
        Optional<Clients> optionalApp = clientsRepository.findById(id);
        if (optionalApp.isPresent()) {
            return optionalApp.get();
        } else {
            throw new JournalNotFoundException("Client not found");
        }
    }

    @Override
    public Clients addClient(Clients client) {
        return clientsRepository.save(client);
    }
}
