#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "FNAFGameManager.generated.h"

UENUM(BlueprintType)
enum class EGameState : uint8
{
    Menu = 0 UMETA(DisplayName = "Menu"),
    NightActive = 1 UMETA(DisplayName = "Night Active"),
    GameOver = 2 UMETA(DisplayName = "Game Over"),
    NightComplete = 3 UMETA(DisplayName = "Night Complete")
};

UCLASS()
class FNAF_LITE_API AFNAFGameManager : public AActor
{
    GENERATED_BODY()

public:
    AFNAFGameManager();

    virtual void Tick(float DeltaTime) override;
    virtual void BeginPlay() override;

    // Game state
    UFUNCTION(BlueprintPure, Category = "Game")
    EGameState GetGameState() const { return CurrentGameState; }

    // Current night
    UFUNCTION(BlueprintPure, Category = "Game")
    int32 GetCurrentNight() const { return CurrentNight; }

    // Time management
    UFUNCTION(BlueprintPure, Category = "Game")
    float GetNightTime() const { return NightTime; }

    UFUNCTION(BlueprintPure, Category = "Game")
    int32 GetHour() const { return FMath::FloorToInt(NightTime / 3600.0f) + 12; }

    // Power management
    UFUNCTION(BlueprintPure, Category = "Power")
    float GetPowerPercentage() const { return (CurrentPower / MaxPower) * 100.0f; }

    // Start new night
    UFUNCTION(BlueprintCallable, Category = "Game")
    void StartNight(int32 NightNumber);

    // Game over
    UFUNCTION(BlueprintCallable, Category = "Game")
    void GameOver();

    // Complete night
    UFUNCTION(BlueprintCallable, Category = "Game")
    void CompleteNight();

    // Power consumption
    UFUNCTION(BlueprintCallable, Category = "Power")
    void ConsumePower(float Amount);

protected:
    // Game state
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    EGameState CurrentGameState;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    int32 CurrentNight;

    // Time tracking (in seconds)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    float NightTime;

    UPROPERTY(EditDefaultsOnly, Category = "Game")
    float NightDuration;

    UPROPERTY(EditDefaultsOnly, Category = "Game")
    float TimeScale;

    // Power system
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Power")
    float CurrentPower;

    UPROPERTY(EditDefaultsOnly, Category = "Power")
    float MaxPower;

    UPROPERTY(EditDefaultsOnly, Category = "Power")
    float PowerDrainRate;

    // Last hour for event triggering
    int32 LastHour;

    // Update game state
    void UpdateGameState();
};
