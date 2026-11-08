package com.carrental.review.domain;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Document(collection = "reviews")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Review {
    @Id
    private String id;

    private Long userId;
    private ReviewTargetType targetType;
    private Long targetId;
    private Integer rating; // 1 à 5
    private String comment;

    @Builder.Default
    private ModerationStatus status = ModerationStatus.APPROVED;

    @Builder.Default
    private LocalDateTime createdAt = LocalDateTime.now();
}
