package com.carrental.review.dto;

import com.carrental.review.domain.ReviewTargetType;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReviewRequest {
    @NotNull
    private Long userId;

    @NotNull
    private ReviewTargetType targetType;

    @NotNull
    private Long targetId;

    @NotNull
    @Min(1) @Max(5)
    private Integer rating;

    private String comment;
}
