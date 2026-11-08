package com.carrental.vehicle.service;

import com.carrental.vehicle.domain.VehicleStatus;
import com.carrental.vehicle.dto.*;
import java.util.List;

public interface VehicleService {
    List<VehicleDTO> getAllVehicles();
    VehicleDTO getVehicleById(Long id);
    List<VehicleDTO> searchVehicles(String brand, Long agencyId);
    AvailabilityResponse checkAvailability(Long id);
    VehicleDTO createVehicle(VehicleDTO dto);
    VehicleDTO updateVehicle(Long id, VehicleDTO dto);
    VehicleDTO updateStatus(Long id, VehicleStatus status);
    void deleteVehicle(Long id);
}
