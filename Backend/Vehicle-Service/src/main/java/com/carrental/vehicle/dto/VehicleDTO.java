package com.carrental.vehicle.dto;

import com.carrental.vehicle.domain.VehicleStatus;
import lombok.*;
import java.math.BigDecimal;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class VehicleDTO {
    private Long id;
    private String brand;
    private String model;
    private Integer year;
    private String licensePlate;
    private String color;
    private Integer seatingCapacity;
    private String transmission;
    private String fuelType;
    private BigDecimal pricePerDay;
    private Double mileage;
    private VehicleStatus status;
    private Long agencyId;
    private String imageUrl;
}
