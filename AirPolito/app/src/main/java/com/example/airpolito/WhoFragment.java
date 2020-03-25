package com.example.airpolito;

import android.content.Context;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import java.io.IOException;
import java.io.InputStream;


public class WhoFragment extends Fragment {

    private ImageView ivAntonio;
    private ImageView ivRasoul;
    private ImageView ivDuilio;
    private ImageView ivArman;

    public WhoFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_who, container, false);

        ivAntonio = view.findViewById(R.id.iv_antonio_photo);
        ivRasoul = view.findViewById(R.id.iv_rasol_photo);
        ivDuilio = view.findViewById(R.id.iv_duilio_photo);
        ivArman = view.findViewById(R.id.iv_arman_photo);

        ivAntonio.setImageBitmap(getImageFromAssetsFile(getContext(),"antonio.jpg"));
        ivRasoul.setImageBitmap(getImageFromAssetsFile(getContext(),"rasol.jpg"));
        ivDuilio.setImageBitmap(getImageFromAssetsFile(getContext(),"duilio.jpg"));
        ivArman.setImageBitmap(getImageFromAssetsFile(getContext(),"arman.jpg"));
        // Inflate the layout for this fragment
        return view;
    }


    public static Bitmap getImageFromAssetsFile(Context mContext, String fileName) {
        Bitmap image = null;
        AssetManager am = mContext.getResources().getAssets();
        try {
            InputStream is = am.open(fileName);
            image = BitmapFactory.decodeStream(is);
            is.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return image;
    }


}
