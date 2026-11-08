package com.carrental.vehicle.repository;

import com.carrental.vehicle.domain.Vehicle;
import com.carrental.vehicle.domain.VehicleStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {
    List<Vehicle> findByAgencyId(Long agencyId);
    List<Vehicle> findByStatus(VehicleStatus status);
    List<Vehicle> findByBrandContainingIgnoreCase(String brand);
}
