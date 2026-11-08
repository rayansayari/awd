package com.carrental.vehicle.service.impl;

import com.carrental.vehicle.domain.Vehicle;
import com.carrental.vehicle.domain.VehicleStatus;
import com.carrental.vehicle.dto.*;
import com.carrental.vehicle.repository.VehicleRepository;
import com.carrental.vehicle.service.VehicleService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class VehicleServiceImpl implements VehicleService {
    private final VehicleRepository vehicleRepository;

    @Override
    public List<VehicleDTO> getAllVehicles() {
        return vehicleRepository.findAll().stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    public VehicleDTO getVehicleById(Long id) {
        Vehicle v = vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Véhicule introuvable: " + id));
        return mapToDTO(v);
    }

    @Override
    public List<VehicleDTO> searchVehicles(String brand, Long agencyId) {
        if (agencyId != null) {
            return vehicleRepository.findByAgencyId(agencyId).stream().map(this::mapToDTO).collect(Collectors.toList());
        }
        if (brand != null && !brand.isBlank()) {
            return vehicleRepository.findByBrandContainingIgnoreCase(brand).stream().map(this::mapToDTO).collect(Collectors.toList());
        }
        return getAllVehicles();
    }

    @Override
    public AvailabilityResponse checkAvailability(Long id) {
        Vehicle v = vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Véhicule introuvable: " + id));
        boolean avail = v.getStatus() == VehicleStatus.AVAILABLE;
        return AvailabilityResponse.builder()
                .vehicleId(v.getId())
                .available(avail)
                .pricePerDay(v.getPricePerDay())
                .message(avail ? "Véhicule disponible" : "Véhicule actuellement indisponible (" + v.getStatus() + ")")
                .build();
    }

    @Override
    public VehicleDTO createVehicle(VehicleDTO dto) {
        Vehicle v = Vehicle.builder()
                .brand(dto.getBrand())
                .model(dto.getModel())
                .year(dto.getYear())
                .licensePlate(dto.getLicensePlate())
                .color(dto.getColor())
                .seatingCapacity(dto.getSeatingCapacity())
                .transmission(dto.getTransmission())
                .fuelType(dto.getFuelType())
                .pricePerDay(dto.getPricePerDay())
                .mileage(dto.getMileage())
                .status(dto.getStatus() != null ? dto.getStatus() : VehicleStatus.AVAILABLE)
                .agencyId(dto.getAgencyId())
                .imageUrl(dto.getImageUrl())
                .build();
        return mapToDTO(vehicleRepository.save(v));
    }

    @Override
    public VehicleDTO updateVehicle(Long id, VehicleDTO dto) {
        Vehicle v = vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Véhicule introuvable: " + id));
        v.setBrand(dto.getBrand());
        v.setModel(dto.getModel());
        v.setPricePerDay(dto.getPricePerDay());
        v.setImageUrl(dto.getImageUrl());
        return mapToDTO(vehicleRepository.save(v));
    }

    @Override
    public VehicleDTO updateStatus(Long id, VehicleStatus status) {
        Vehicle v = vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Véhicule introuvable: " + id));
        v.setStatus(status);
        return mapToDTO(vehicleRepository.save(v));
    }

    @Override
    public void deleteVehicle(Long id) {
        vehicleRepository.deleteById(id);
    }

    private VehicleDTO mapToDTO(Vehicle v) {
        return VehicleDTO.builder()
                .id(v.getId())
                .brand(v.getBrand())
                .model(v.getModel())
                .year(v.getYear())
                .licensePlate(v.getLicensePlate())
                .color(v.getColor())
                .seatingCapacity(v.getSeatingCapacity())
                .transmission(v.getTransmission())
                .fuelType(v.getFuelType())
                .pricePerDay(v.getPricePerDay())
                .mileage(v.getMileage())
                .status(v.getStatus())
                .agencyId(v.getAgencyId())
                .imageUrl(v.getImageUrl())
                .build();
    }
}
