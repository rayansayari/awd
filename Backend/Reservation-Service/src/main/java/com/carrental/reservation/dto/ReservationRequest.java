package com.carrental.reservation.dto;

import jakarta.validation.constraints.NotNull;
import lombok.*;
import java.time.LocalDate;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReservationRequest {
    @NotNull
    private Long userId;

    @NotNull
    private Long vehicleId;

    private Long pickupAgencyId;
    private Long returnAgencyId;

    @NotNull
    private LocalDate startDate;

    @NotNull
    private LocalDate endDate;

    private String notes;
}
