#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "FNAFAnimatronic.generated.h"

UENUM(BlueprintType)
enum class EAnimatronicState : uint8
{
    Idle = 0 UMETA(DisplayName = "Idle"),
    Moving = 1 UMETA(DisplayName = "Moving"),
    Attacking = 2 UMETA(DisplayName = "Attacking"),
    Disabled = 3 UMETA(DisplayName = "Disabled")
};

UCLASS()
class FNAF_LITE_API AFNAFAnimatronic : public ACharacter
{
    GENERATED_BODY()

public:
    AFNAFAnimatronic();

    virtual void Tick(float DeltaTime) override;
    virtual void BeginPlay() override;

    // State management
    UFUNCTION(BlueprintPure, Category = "Animatronic")
    EAnimatronicState GetState() const { return CurrentState; }

    UFUNCTION(BlueprintCallable, Category = "Animatronic")
    void SetState(EAnimatronicState NewState);

    // Animation control
    UFUNCTION(BlueprintCallable, Category = "Animation")
    void PlayAttackAnimation();

    UFUNCTION(BlueprintCallable, Category = "Animation")
    void PlayIdleAnimation();

    // Movement
    UFUNCTION(BlueprintCallable, Category = "Movement")
    void MoveToLocation(FVector TargetLocation);

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StopMovement();

    // AI behavior
    UFUNCTION(BlueprintCallable, Category = "AI")
    void UpdateAI(float DeltaTime);

    // Get animatronic name
    UFUNCTION(BlueprintPure, Category = "Animatronic")
    FString GetAnimatronicName() const { return AnimatronicName; }

protected:
    // Animatronic properties
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animatronic")
    FString AnimatronicName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animatronic")
    int32 StartingPosition;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Animatronic")
    int32 CurrentPosition;

    // State
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Animatronic")
    EAnimatronicState CurrentState;

    // AI properties
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI")
    float AggressionLevel;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI")
    float MovementSpeed;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI")
    float MoveUpdateInterval;

    // Timing
    float TimeSinceLastMove;
    float TimeSinceStateChange;

    // Attack range
    UPROPERTY(EditDefaultsOnly, Category = "AI")
    float AttackRange;

    // Update AI logic based on aggression level
    void UpdateAIBehavior(float DeltaTime);
};
