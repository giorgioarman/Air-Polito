package com.ArmaniDio.airpolito;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;


public class IpqaFragment extends Fragment {

    public IpqaFragment() {
        // Required empty public constructor
    }

    private WebView webView;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_ipqa, container, false);

        webView = view.findViewById(R.id.wv_ipqa_details);

        webView.loadUrl("file:///android_asset/ipqa_details.html");
        // Inflate the layout for this fragment
        return view;
    }

}
