package com.carrental.review.service.impl;

import com.carrental.review.domain.*;
import com.carrental.review.dto.*;
import com.carrental.review.repository.ReviewRepository;
import com.carrental.review.service.ReviewService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ReviewServiceImpl implements ReviewService {
    private final ReviewRepository reviewRepository;

    @Override
    public ReviewResponse createReview(ReviewRequest req) {
        Review r = Review.builder()
                .userId(req.getUserId())
                .targetType(req.getTargetType())
                .targetId(req.getTargetId())
                .rating(req.getRating())
                .comment(req.getComment())
                .status(ModerationStatus.APPROVED)
                .build();
        return mapToDTO(reviewRepository.save(r));
    }

    @Override
    public List<ReviewResponse> getReviewsByTarget(ReviewTargetType type, Long targetId) {
        return reviewRepository.findByTargetTypeAndTargetId(type, targetId)
                .stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    public List<ReviewResponse> getReviewsByUser(Long userId) {
        return reviewRepository.findByUserId(userId)
                .stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    private ReviewResponse mapToDTO(Review r) {
        return ReviewResponse.builder()
                .id(r.getId())
                .userId(r.getUserId())
                .targetType(r.getTargetType())
                .targetId(r.getTargetId())
                .rating(r.getRating())
                .comment(r.getComment())
                .status(r.getStatus())
                .createdAt(r.getCreatedAt())
                .build();
    }
}
