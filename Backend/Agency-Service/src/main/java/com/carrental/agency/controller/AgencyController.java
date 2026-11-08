package com.carrental.agency.controller;

import com.carrental.agency.dto.AgencyDTO;
import com.carrental.agency.service.AgencyService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/agencies")
@RequiredArgsConstructor
public class AgencyController {
    private final AgencyService agencyService;

    @GetMapping
    public ResponseEntity<List<AgencyDTO>> getAll() {
        return ResponseEntity.ok(agencyService.getAllAgencies());
    }

    @GetMapping("/{id}")
    public ResponseEntity<AgencyDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(agencyService.getAgencyById(id));
    }

    @GetMapping("/city/{city}")
    public ResponseEntity<List<AgencyDTO>> getByCity(@PathVariable String city) {
        return ResponseEntity.ok(agencyService.getAgenciesByCity(city));
    }

    @PostMapping
    public ResponseEntity<AgencyDTO> create(@RequestBody AgencyDTO dto) {
        return new ResponseEntity<>(agencyService.createAgency(dto), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<AgencyDTO> update(@PathVariable Long id, @RequestBody AgencyDTO dto) {
        return ResponseEntity.ok(agencyService.updateAgency(id, dto));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        agencyService.deleteAgency(id);
        return ResponseEntity.noContent().build();
    }
}
