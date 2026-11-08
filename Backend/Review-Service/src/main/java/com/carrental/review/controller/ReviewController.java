package com.carrental.review.controller;

import com.carrental.review.domain.ReviewTargetType;
import com.carrental.review.dto.*;
import com.carrental.review.service.ReviewService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/reviews")
@RequiredArgsConstructor
public class ReviewController {
    private final ReviewService reviewService;

    @PostMapping
    public ResponseEntity<ReviewResponse> create(@Valid @RequestBody ReviewRequest req) {
        return new ResponseEntity<>(reviewService.createReview(req), HttpStatus.CREATED);
    }

    @GetMapping("/vehicle/{vehicleId}")
    public ResponseEntity<List<ReviewResponse>> getByVehicle(@PathVariable Long vehicleId) {
        return ResponseEntity.ok(reviewService.getReviewsByTarget(ReviewTargetType.VEHICLE, vehicleId));
    }

    @GetMapping("/agency/{agencyId}")
    public ResponseEntity<List<ReviewResponse>> getByAgency(@PathVariable Long agencyId) {
        return ResponseEntity.ok(reviewService.getReviewsByTarget(ReviewTargetType.AGENCY, agencyId));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<ReviewResponse>> getByUser(@PathVariable Long userId) {
        return ResponseEntity.ok(reviewService.getReviewsByUser(userId));
    }
}
