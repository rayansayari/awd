package com.carrental.review.service;

import com.carrental.review.domain.ReviewTargetType;
import com.carrental.review.dto.*;
import java.util.List;

public interface ReviewService {
    ReviewResponse createReview(ReviewRequest req);
    List<ReviewResponse> getReviewsByTarget(ReviewTargetType type, Long targetId);
    List<ReviewResponse> getReviewsByUser(Long userId);
}
