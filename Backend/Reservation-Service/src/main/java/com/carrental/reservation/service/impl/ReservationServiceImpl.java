package com.carrental.reservation.service.impl;

import com.carrental.reservation.client.PaymentClient;
import com.carrental.reservation.client.VehicleClient;
import com.carrental.reservation.domain.Reservation;
import com.carrental.reservation.domain.ReservationStatus;
import com.carrental.reservation.dto.*;
import com.carrental.reservation.repository.ReservationRepository;
import com.carrental.reservation.service.ReservationService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ReservationServiceImpl implements ReservationService {
    private final ReservationRepository reservationRepository;
    private final VehicleClient vehicleClient;
    private final PaymentClient paymentClient;

    @Override
    public ReservationResponse createReservation(ReservationRequest req) {
        long days = ChronoUnit.DAYS.between(req.getStartDate(), req.getEndDate());
        if (days <= 0) days = 1;

        BigDecimal dailyRate = BigDecimal.valueOf(50.0);
        try {
            Map<String, Object> vehicle = vehicleClient.getVehicleById(req.getVehicleId());
            if (vehicle != null && vehicle.containsKey("pricePerDay")) {
                dailyRate = new BigDecimal(vehicle.get("pricePerDay").toString());
            }
        } catch (Exception ignored) {
            // Fallback si Vehicle-Service en test
        }

        BigDecimal total = dailyRate.multiply(BigDecimal.valueOf(days));

        Reservation res = Reservation.builder()
                .reservationNumber("RES-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase())
                .userId(req.getUserId())
                .vehicleId(req.getVehicleId())
                .pickupAgencyId(req.getPickupAgencyId())
                .returnAgencyId(req.getReturnAgencyId())
                .startDate(req.getStartDate())
                .endDate(req.getEndDate())
                .totalDays(days)
                .dailyRate(dailyRate)
                .totalPrice(total)
                .status(ReservationStatus.PENDING)
                .notes(req.getNotes())
                .build();

        Reservation saved = reservationRepository.save(res);

        // Simulation de paiement immédiat
        try {
            paymentClient.processPayment(Map.of(
                "reservationId", saved.getId(),
                "userId", saved.getUserId(),
                "amount", total,
                "method", "CREDIT_CARD"
            ));
            saved.setStatus(ReservationStatus.CONFIRMED);
            reservationRepository.save(saved);
        } catch (Exception ignored) {}

        return mapToDTO(saved);
    }

    @Override
    public ReservationResponse getReservationById(Long id) {
        return reservationRepository.findById(id)
                .map(this::mapToDTO)
                .orElseThrow(() -> new RuntimeException("Réservation introuvable: " + id));
    }

    @Override
    public List<ReservationResponse> getUserReservations(Long userId) {
        return reservationRepository.findByUserId(userId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    public ReservationResponse confirmReservation(Long id) {
        Reservation res = reservationRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Réservation introuvable: " + id));
        res.setStatus(ReservationStatus.CONFIRMED);
        return mapToDTO(reservationRepository.save(res));
    }

    @Override
    public ReservationResponse cancelReservation(Long id) {
        Reservation res = reservationRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Réservation introuvable: " + id));
        res.setStatus(ReservationStatus.CANCELLED);
        return mapToDTO(reservationRepository.save(res));
    }

    private ReservationResponse mapToDTO(Reservation r) {
        return ReservationResponse.builder()
                .id(r.getId())
                .reservationNumber(r.getReservationNumber())
                .userId(r.getUserId())
                .vehicleId(r.getVehicleId())
                .pickupAgencyId(r.getPickupAgencyId())
                .returnAgencyId(r.getReturnAgencyId())
                .startDate(r.getStartDate())
                .endDate(r.getEndDate())
                .totalDays(r.getTotalDays())
                .dailyRate(r.getDailyRate())
                .totalPrice(r.getTotalPrice())
                .status(r.getStatus())
                .build();
    }
}
