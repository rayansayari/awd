package com.carrental.vehicle.dto;

import lombok.*;
import java.math.BigDecimal;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class AvailabilityResponse {
    private Long vehicleId;
    private Boolean available;
    private BigDecimal pricePerDay;
    private String message;
}
