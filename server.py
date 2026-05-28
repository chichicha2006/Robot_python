import asyncio
import websockets
import json
import mbassem



async def handler(websocket):

    print("Unity connecté !")

    async for message in websocket:

        try:

            data = json.loads(message) # récupère depuis Unity via websocket

            #recupere le json envoyé depuis unity 
            headLF = data["headLF"]
            headUD = data["headUD"]

            rightArmSide = data["rightArmSide"]
            rightArm = data["rightArm"]
            rightLowerArm = data["rightLowerArm"]

           # leftArmSide = data["leftArmSide"]
            #leftArm = data["leftArm"]
            #leftLowerArm = data["leftLowerArm"]

            #affichage
            print("Head LF :", headLF)
            print("Head UD :", headUD)

            print("Right Arm Side :", rightArmSide)
            print("Right Arm :", rightArm)
            print("Right Lower Arm :", rightLowerArm)

         #   print("Left Arm Side :", leftArmSide)
         #   print("Left Arm :", leftArm)
         #   print("Left Lower Arm :", leftLowerArm)
            
            

            mbassem.move_headLF(headLF)
            mbassem.move_headUD(headUD)

            mbassem.move_rightArmSide(rightArmSide)
            mbassem.move_rightArm(rightArm)
            mbassem.move_rightLowerArm(rightLowerArm)
            
            print("------------------------------------------------------------------------")
    

           # mbassem.move_leftArmSide(leftArmSide)
           # mbassem.move_leftArm(leftArm)
           # mbassem.move_leftLowerArm(leftLowerArm)

        except Exception as e:

            print("Erreur :", e)


async def main():

    server = await websockets.serve(handler, "localhost", 8765)

    print("Serveur lancé")

    await server.wait_closed()

asyncio.run(main())