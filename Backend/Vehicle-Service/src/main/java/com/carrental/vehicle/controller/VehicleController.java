package com.carrental.vehicle.controller;

import com.carrental.vehicle.domain.VehicleStatus;
import com.carrental.vehicle.dto.*;
import com.carrental.vehicle.service.VehicleService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/vehicles")
@RequiredArgsConstructor
public class VehicleController {
    private final VehicleService vehicleService;

    @GetMapping
    public ResponseEntity<List<VehicleDTO>> getAll() {
        return ResponseEntity.ok(vehicleService.getAllVehicles());
    }

    @GetMapping("/{id}")
    public ResponseEntity<VehicleDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(vehicleService.getVehicleById(id));
    }

    @GetMapping("/search")
    public ResponseEntity<List<VehicleDTO>> search(
            @RequestParam(required = false) String brand,
            @RequestParam(required = false) Long agencyId) {
        return ResponseEntity.ok(vehicleService.searchVehicles(brand, agencyId));
    }

    @GetMapping("/{id}/availability")
    public ResponseEntity<AvailabilityResponse> checkAvailability(@PathVariable Long id) {
        return ResponseEntity.ok(vehicleService.checkAvailability(id));
    }

    @PostMapping
    public ResponseEntity<VehicleDTO> create(@RequestBody VehicleDTO dto) {
        return new ResponseEntity<>(vehicleService.createVehicle(dto), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<VehicleDTO> update(@PathVariable Long id, @RequestBody VehicleDTO dto) {
        return ResponseEntity.ok(vehicleService.updateVehicle(id, dto));
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<VehicleDTO> updateStatus(@PathVariable Long id, @RequestParam VehicleStatus status) {
        return ResponseEntity.ok(vehicleService.updateStatus(id, status));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        vehicleService.deleteVehicle(id);
        return ResponseEntity.noContent().build();
    }
}
