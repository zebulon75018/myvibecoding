#!/usr/bin/env python3
"""
Script pour générer une vidéo de test colorée
Utile pour tester l'application sans avoir de vidéo sous la main
"""

import ffmpeg
import os

def create_test_video(output_path="test_video.mp4", duration=10, width=1280, height=720):
    """
    Crée une vidéo de test colorée avec un compteur de temps
    
    Args:
        output_path: Chemin du fichier de sortie
        duration: Durée de la vidéo en secondes
        width: Largeur de la vidéo
        height: Hauteur de la vidéo
    """
    
    print(f"Génération d'une vidéo de test...")
    print(f"  - Durée: {duration}s")
    print(f"  - Résolution: {width}x{height}")
    print(f"  - Fichier: {output_path}")
    
    try:
        # Générer une vidéo avec un pattern de test coloré et un compteur
        (
            ffmpeg
            .input('testsrc=duration={}:size={}x{}:rate=30'.format(duration, width, height), 
                   f='lavfi')
            .output(output_path, 
                    vcodec='libx264',
                    pix_fmt='yuv420p',
                    preset='fast',
                    crf=23)
            .overwrite_output()
            .run(quiet=True)
        )
        
        print(f"✅ Vidéo de test créée: {output_path}")
        print(f"   Taille du fichier: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
        
    except ffmpeg.Error as e:
        print(f"❌ Erreur lors de la création de la vidéo de test:")
        print(e.stderr.decode())

def create_colorful_video(output_path="colorful_test.mp4", duration=5):
    """
    Crée une vidéo avec des transitions de couleurs
    """
    print(f"Génération d'une vidéo colorée...")
    
    try:
        # Créer une vidéo avec des couleurs changeantes
        (
            ffmpeg
            .input('color=c=red:duration={}:s=1280x720:r=30'.format(duration/3), 
                   f='lavfi')
            .filter('fade', type='out', start_time=duration/3-1, duration=1)
            .output('temp_red.mp4', vcodec='libx264', pix_fmt='yuv420p')
            .overwrite_output()
            .run(quiet=True)
        )
        
        (
            ffmpeg
            .input('color=c=green:duration={}:s=1280x720:r=30'.format(duration/3), 
                   f='lavfi')
            .filter('fade', type='in', duration=1)
            .filter('fade', type='out', start_time=duration/3-1, duration=1)
            .output('temp_green.mp4', vcodec='libx264', pix_fmt='yuv420p')
            .overwrite_output()
            .run(quiet=True)
        )
        
        (
            ffmpeg
            .input('color=c=blue:duration={}:s=1280x720:r=30'.format(duration/3), 
                   f='lavfi')
            .filter('fade', type='in', duration=1)
            .output('temp_blue.mp4', vcodec='libx264', pix_fmt='yuv420p')
            .overwrite_output()
            .run(quiet=True)
        )
        
        # Concaténer les vidéos
        with open('concat_list.txt', 'w') as f:
            f.write("file 'temp_red.mp4'\n")
            f.write("file 'temp_green.mp4'\n")
            f.write("file 'temp_blue.mp4'\n")
        
        (
            ffmpeg
            .input('concat_list.txt', format='concat', safe=0)
            .output(output_path, c='copy')
            .overwrite_output()
            .run(quiet=True)
        )
        
        # Nettoyer les fichiers temporaires
        os.remove('temp_red.mp4')
        os.remove('temp_green.mp4')
        os.remove('temp_blue.mp4')
        os.remove('concat_list.txt')
        
        print(f"✅ Vidéo colorée créée: {output_path}")
        
    except ffmpeg.Error as e:
        print(f"❌ Erreur lors de la création de la vidéo colorée:")
        print(e.stderr.decode())

if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("  Générateur de vidéos de test")
    print("=" * 50)
    print()
    
    # Vérifier si ffmpeg est disponible
    try:
        ffmpeg.probe('test')
    except:
        pass
    
    # Menu
    print("Choisissez le type de vidéo à générer:")
    print("1. Vidéo de test standard (pattern coloré)")
    print("2. Vidéo avec transitions de couleurs")
    print("3. Les deux")
    print()
    
    choice = input("Votre choix (1-3): ").strip()
    
    if choice == '1':
        create_test_video()
    elif choice == '2':
        create_colorful_video()
    elif choice == '3':
        create_test_video()
        create_colorful_video()
    else:
        print("Choix invalide. Génération de la vidéo standard...")
        create_test_video()
    
    print()
    print("✅ Terminé! Vous pouvez maintenant utiliser ces vidéos pour tester l'application.")
