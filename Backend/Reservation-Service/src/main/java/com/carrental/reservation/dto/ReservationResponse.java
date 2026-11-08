package com.carrental.reservation.dto;

import com.carrental.reservation.domain.ReservationStatus;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDate;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReservationResponse {
    private Long id;
    private String reservationNumber;
    private Long userId;
    private Long vehicleId;
    private Long pickupAgencyId;
    private Long returnAgencyId;
    private LocalDate startDate;
    private LocalDate endDate;
    private Long totalDays;
    private BigDecimal dailyRate;
    private BigDecimal totalPrice;
    private ReservationStatus status;
}
