#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "FNAFPlayerController.generated.h"

UCLASS()
class FNAF_LITE_API AFNAFPlayerController : public APlayerController
{
    GENERATED_BODY()

public:
    AFNAFPlayerController();

    virtual void SetupInput(class UInputComponent* PlayerInputComponent) override;
    virtual void BeginPlay() override;

    // Camera switching
    UFUNCTION(BlueprintCallable, Category = "Camera")
    void SwitchCamera(int32 CameraIndex);

    // Door control
    UFUNCTION(BlueprintCallable, Category = "Door")
    void ToggleDoor(int32 DoorID, bool bOpen);

    // Light control
    UFUNCTION(BlueprintCallable, Category = "Light")
    void ToggleLight(int32 LightID, bool bOn);

    // Get current camera
    UFUNCTION(BlueprintPure, Category = "Camera")
    int32 GetCurrentCamera() const { return CurrentCameraIndex; }

    // Get power level
    UFUNCTION(BlueprintPure, Category = "Power")
    float GetPowerLevel() const { return PowerLevel; }

    // Update power
    UFUNCTION(BlueprintCallable, Category = "Power")
    void UpdatePower(float Amount);

protected:
    // Current active camera
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
    int32 CurrentCameraIndex;

    // Power level (0-100)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Power")
    float PowerLevel;

    // Active doors (bitmask)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Door")
    uint32 ActiveDoors;

    // Active lights (bitmask)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Light")
    uint32 ActiveLights;

    // Power consumption rates
    UPROPERTY(EditDefaultsOnly, Category = "Power")
    float CameraPowerCost;

    UPROPERTY(EditDefaultsOnly, Category = "Power")
    float DoorPowerCost;

    UPROPERTY(EditDefaultsOnly, Category = "Power")
    float LightPowerCost;
};
