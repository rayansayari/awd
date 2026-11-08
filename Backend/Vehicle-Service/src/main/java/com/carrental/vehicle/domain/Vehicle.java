package com.carrental.vehicle.domain;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "vehicles")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Vehicle {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String brand;

    @Column(nullable = false)
    private String model;

    private Integer year;

    @Column(nullable = false, unique = true)
    private String licensePlate;

    private String color;
    private Integer seatingCapacity;
    private String transmission;
    private String fuelType;

    @Column(nullable = false)
    private BigDecimal pricePerDay;

    private Double mileage;

    @Enumerated(EnumType.STRING)
    @Builder.Default
    private VehicleStatus status = VehicleStatus.AVAILABLE;

    private Long agencyId;
    private String imageUrl;

    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}
