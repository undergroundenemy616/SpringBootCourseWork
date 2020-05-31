package main.web;

import main.entity.BookTypes;
import main.entity.Clients;
import main.exception.JournalNotFoundException;
import main.repository.BookTypesRepository;
import main.repository.ClientsRepository;
import main.service.ClientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;

@org.springframework.web.bind.annotation.RestController
@RequestMapping("/libr")
public class ClientsController {

    @Autowired
    private ClientsRepository clientsRepository;

    private ClientService clientService;

    @PostMapping(value = "/addClient")
    public Clients addClient(@RequestBody Clients newClient){
        return clientService.addClient(newClient);
    }

    @PutMapping("/editClient/{id}")
    public ResponseEntity<Object> updateClient(@RequestBody Clients newClient, @PathVariable Integer id) {
        Optional<Clients> clientOptional = clientsRepository.findById(id);
        if (!clientOptional.isPresent())
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Client not found");
        newClient.setId(id);
        clientsRepository.save(newClient);
        return new ResponseEntity<>(newClient, HttpStatus.OK);
    }

    @GetMapping("/clients")
    public ResponseEntity<List<Clients>> getAllClients(){
        List<Clients> list = clientService.listClients();
        return new ResponseEntity<>(list, HttpStatus.OK);
    }

    @GetMapping("/client/{id}")
    public ResponseEntity<Clients> getClient(@PathVariable("id") Integer id){
        Optional<Clients> clientOptional = clientsRepository.findById(id);
        try{
            return new ResponseEntity<>(clientService.findClient(id), HttpStatus.OK);
        } catch (JournalNotFoundException exception) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Client not found");
        }
    }

    @DeleteMapping("/deleteClient/{id}")
    public boolean deleteClient(@PathVariable Integer id) {
        clientsRepository.deleteById(id);
        return true;
    }


    @Autowired
    public void setClientService(ClientService clientService) {
        this.clientService = clientService;
    }
}
