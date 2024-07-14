package com.example.user_activities.services;

import com.example.user_activities.model.Activity;
import com.example.user_activities.repository.ActivityRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class ActivityService {

    @Autowired
    private ActivityRepository activityRepository;

    @Autowired
    private KafkaProducerService kafkaProducerService;

    public Mono<Activity> saveActivity(Activity activity) {
        return activityRepository.save(activity)
                .doOnSuccess(savedActivity -> kafkaProducerService.sendMessage("activity-topic", "Actividad creada: " + savedActivity.getId()));
    }

    public Mono<Activity> findById(Long id) {
        return activityRepository.findById(id);
    }

    public Flux<Activity> findAll() {
        return activityRepository.findAll();
    }

    public Mono<Activity> updateActivity(Long id, Activity activity) {
        return activityRepository.findById(id)
                .flatMap(existingActivity -> {
                    existingActivity.setAction(activity.getAction());
                    existingActivity.setUserId(activity.getUserId());
                    existingActivity.setBookId(activity.getBookId());
                    existingActivity.setDueDate(activity.getDueDate());
                    existingActivity.setFine(activity.getFine());
                    return activityRepository.save(existingActivity)
                            .doOnSuccess(updatedActivity -> kafkaProducerService.sendMessage("activity-topic", "Actividad actualizada: " + updatedActivity.getId()));
                });
    }

    public Mono<Void> deleteActivity(Long id) {
        return activityRepository.findById(id)
                .flatMap(existingActivity ->
                        activityRepository.delete(existingActivity)
                                .then(Mono.fromRunnable(() -> kafkaProducerService.sendMessage("activity-topic", "Actividad eliminada: " + existingActivity.getId())))
                );
    }
}
