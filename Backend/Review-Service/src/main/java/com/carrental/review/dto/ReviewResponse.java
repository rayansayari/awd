package com.carrental.review.dto;

import com.carrental.review.domain.ModerationStatus;
import com.carrental.review.domain.ReviewTargetType;
import lombok.*;
import java.time.LocalDateTime;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReviewResponse {
    private Long id;
    private Long userId;
    private ReviewTargetType targetType;
    private Long targetId;
    private Integer rating;
    private String comment;
    private ModerationStatus status;
    private LocalDateTime createdAt;
}
