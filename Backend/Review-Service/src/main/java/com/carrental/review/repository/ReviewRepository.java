package com.carrental.review.repository;

import com.carrental.review.domain.Review;
import com.carrental.review.domain.ReviewTargetType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByTargetTypeAndTargetId(ReviewTargetType targetType, Long targetId);
    List<Review> findByUserId(Long userId);
}
